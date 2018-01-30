# -*- coding: utf-8 -*-

import logging

from django.core.urlresolvers import reverse
from site_checker_app import settings_app
from site_checker_app.models import CheckSite


log = logging.getLogger(__name__)


def checkSiteV2( site ):
  '''
  - Purpose: check a checkSite entry.
  - Called by: checkSites(), which is called from cronscript, and tests.UtilityCodeTests()
  '''
  try:
    ## setup
    import requests
    log.debug( u'- in uc.checkSiteV2(); starting' )
    # from django.utils.encoding import smart_unicode
    import datetime, random, sys
    log_identifier = 'li_%s' % random.randint(1000,9999)
    ## access site
    return_val = u'init'
    log.debug( u'- in uc.checkSiteV2(); trying site "%s" at "%s"' % (site.name, site.url) )
    try:
      # if type(site.url) == str:
      #   log.debug( u'- in uc.checkSiteV2(); converted url from str to unicode' )
      #   site.url = site.url.decode( u'utf-8', u'replace' )
      r = requests.get( site.url, timeout=30, verify=True )
      log.debug( u'- in uc.checkSiteV2(); url attempted' )
    except:
      message = makeErrorString()
      log.error( u'- in uc.checkSiteV2(); error accessing url; error is: %s' %  message )
      return_val = u'url_not_accessible'
      log.debug( u'- in uc.checkSiteV2(); return_val is: "%s"' % return_val )
    ## read response
    if return_val == u'init':
      try:
        html = r.content.decode( u'utf-8', u'replace' )
        log.debug( u'- in uc.checkSiteV2(); html perceived' )
      except:
        message = makeErrorString()
        log.error( u'- in uc.checkSiteV2(); error reading response; error is: %s' %  message )
        return_val = u'unable_to_read_response'
        log.debug( u'- in uc.checkSiteV2(); return_val is: "%s"' % return_val )
    ## check html
    if return_val == u'init':
      # if type(site.text_expected) == str:
      #   site.text_expected = site.text_expected.decode( u'utf-8', u'replace' )
      #   log.debug( u'- in uc.checkSiteV2(); converted site.text_expected from str to unicode' )
      if site.text_expected in html:
        return_val = u'passed'
      else:
        return_val = u'text_not_found'
      log.debug( u'- in uc.checkSiteV2(); html-check; return_val is: "%s"' % (return_val,) )
    ## update site object
    log.debug( u'- in uc.checkSiteV2(); site info, *before* update: pre_previous_checked_result - "%s"; previous_checked_result - "%s"; recent_checked_result - "%s"; recent_checked_time - "%s".' % (site.pre_previous_checked_result, site.previous_checked_result, site.recent_checked_result, site.recent_checked_time) )
    site.pre_previous_checked_result = site.previous_checked_result
    site.previous_checked_result = site.recent_checked_result
    site.recent_checked_result = return_val
    site.recent_checked_time = datetime.datetime.now()
    site.save()
    log.debug( u'- in uc.checkSiteV2(); site info, *after* update: pre_previous_checked_result - "%s"; previous_checked_result - "%s"; recent_checked_result - "%s"; recent_checked_time - "%s".' % (site.pre_previous_checked_result, site.previous_checked_result, site.recent_checked_result, site.recent_checked_time,) )
    ## return (return_val not read)
    return return_val
  except:
    message = makeErrorString()
    log.error( u'- in uc.checkSiteV2(); main try exception; exception is: %s' %  message )
    return_val = u'failure'
    log.debug( u'- in uc.checkSiteV2(); return_val is: "%s"' % return_val )

  # end def checkSiteV2()



def checkSites( query_dict ):
  '''
  - Purpose: checks each checkSite in the queryset ( determined by grabSitesToCheck() )
  - Called by: cron script
  '''
  try:
    log.debug( u'- in uc.checkSites(); --- starting ---' )
    for site in query_dict:
      ## check the site
      checkSiteV2( site )
      ## send email if necessary
      email_check_result = runEmailCheck( site )
      log.debug( u'- in uc.checkSites(); email_check_result is: "%s"' % email_check_result )
      if email_check_result == 'send_failure_email':
        sendFailureEmail( site )
      elif email_check_result == 'send_success_email':
        sendPassedEmail( site )
    log.debug( u'- in uc.checkSites(); --- checkSites() ending ---' )
    return 'done'
  except:
    error_message = u'- in uc.checkSites(); error_message: %s' % makeErrorString()
    log.error( error_message )
    return error_message

  # end def checkSites()



def grabSitesToCheck( submitted_current_date ):
  '''
  - Purpose: grabs a list of sites that need to be checked based on the current time
  - Called by: cronscript.py, which then passes the sites list to checkSites()
  '''
  try:
    # from site_check_app.models import CheckSite
    log.debug( u'- in uc.grabSitesToCheck(); grabbing sites to check' )
    query_set = CheckSite.objects.filter( next_check_time__lte=submitted_current_date )
    log.debug( u'- in uc.grabSitesToCheck(); number of records grabbed: %s' % (query_set.count(),) )
    return { 'query_set': query_set }
  except:
    error_message = u'- in uc.grabSitesToCheck(); error_message: %s' % makeErrorString()
    log.error( error_message )
    return error_message



def hitSimpleAuth( username, password ):
  '''
  - Purpose: hit simple-auth webservice for authN.
  - Called by: views.handleAdmin()
  '''

  try:
    from django.utils import simplejson
    import urllib, urllib2
    url = '%ssimple_auth/' % settings_app.SIMPLE_AUTH_URL_SEGMENT
    parameter_dict = {
      'username': username,
      'password': password,
      'authorization_key': settings_app.SIMPLE_AUTH_AUTHORIZATION_KEY }
    data = urllib.urlencode( parameter_dict )
    request = urllib2.Request( url, data )
    response = urllib2.urlopen( request )
    data = response.read()
    return_dict = simplejson.loads( data )
    return return_dict
  except:
    message = u'- in uc.hitSimpleAuth(); error is: %s' % makeErrorString()
    log.error( message )
    return { 'status': 'failure' }

  # end def hitSimpleAuth()



def makeErrorString():
  '''
  - Purpose: to return detailed error information.
  - Called by: could be any exception block.
  '''
  import sys
  message = 'error-type - %s; error-message - %s; line-number - %s' % ( sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno, )
  return message[0:1000]
  # end def makeErrorString()



def parseEmailAddresses( email_field_string ):
  '''
  - Purpose: prepare a list of email addresses from the email-field string
  - Called by: sendFailureEmail(), sendPassedEmail()
  '''
  list_a = email_field_string.split(",")
  list_b = []
  for element in list_a:
    # print '-- element-before: "%s" --' % ( element, )
    element = element.strip()
    list_b.append( element )
    # print '-- element-after: "%s" --' % ( element, )
  return list_b

  # end def parseEmailAddresses()


def runEmailCheck( site ):
  '''
  - Purpose: determines whether 'problem' or 'ok' email needs to be sent to user
  - Called by: checkSites() after result of checkSite() is determined
  - Note: use of syntax "if 'passed' in site.the_field" is because
          the value could be 'passed' or 'passed_though_non_unicode'
  '''
  try:
    # Email logic...
    # - Don't send a failure email on the first fail -- it could be a momentary network issue.
    # - Since any failure will increase the check-frequency to (at least) every five minutes, send the failure email on the second failure.
    # - To distinguish a second failure from repeated failues, the pre_previous_checked_result must be 'passed'.
    # - Success testing: send email on a pass where the previous two checks were failures (not on single previous failure to avoid temporary blips).

    # setup
    return_val = 'init'

    # no-email cases
    if (
      'passed' in site.recent_checked_result and
      'passed' in site.previous_checked_result
      ):  # all is well and has been well -- expected most common case
      return_val = 'send_no_email'

    elif (
      'passed' not in site.recent_checked_result and
      'passed' in site.previous_checked_result
      ):  # on current temporary failure -- another expected common case
      return_val = 'send_no_email'
    elif (
      'passed' not in site.recent_checked_result and
      'passed' not in site.previous_checked_result and
      (site.pre_previous_checked_result == 'text_not_found' or site.pre_previous_checked_result == 'url_not_accessible')  # not != 'passed' because an empty string ('') would be a failure condition, and is handled below.
      ):  # on repeated failures -- another expected common case
      return_val = 'send_no_email'
    elif (
      # site.previous_checked_result == ''):  # on initial record-creation, whether first check is successful or not
      site.previous_checked_result == 'init'):  # on initial record-creation, whether first check is successful or not
      return_val = 'send_no_email'
    elif (
      'passed' in site.recent_checked_result and
      'passed' not in site.previous_checked_result and
      'passed' in site.pre_previous_checked_result
      ):  # on current success after temporary failure
      return_val = 'send_no_email'

    # failure-email cases
    elif (
      'passed' not in site.recent_checked_result and
      'passed' not in site.previous_checked_result and
      ('passed' in site.pre_previous_checked_result or site.pre_previous_checked_result == 'init')
      ):
      return_val = 'send_failure_email'

    # success-email cases
    elif (
      'passed' in site.recent_checked_result and
      'passed' not in site.previous_checked_result and
      'passed' not in site.pre_previous_checked_result
      ):
      return_val = 'send_success_email'

    else:
      log.debug( u'- in uc.runEmailCheck(); UNHANDLED condition met (no email will be sent)' )
      return_val = 'UNHANDLED'

    log.debug( u'- in uc.runEmailCheck(); return val is: %s' % return_val )
    return return_val

  except Exception as e:
    log.error( 'exception, ```%s```' % str(e) )
    return 'FAILURE'
    # return { 'status': 'failure' }

  ## end def runEmailCheck()


def sendFailureEmail( site ):
  '''
  - Purpose: sends failure-alert email
  - Called by: checkSites()
  '''
  try:
    from django.core.mail import send_mail
    admin_login_url = '%s%s' % ( settings_app.CHECKER_URL_ROOT, reverse('admin_login_url') )
    subject = 'Service-Status alert: "%s" problem' % ( site.name )
    message = build_failure_email_message( site.name, site.check_frequency_number, site.check_frequency_unit, site.url, site.text_expected, site.email_message, admin_login_url )
    from_address = settings_app.EMAIL_FROM_ADDRESS
    to_address_list = parseEmailAddresses( site.email_addresses )
    send_mail( subject, message, from_address, to_address_list, fail_silently=False )
    log.debug( u'- in uc.sendFailureEmail(); failure email sent' )
    return 'failure email sent'
  except Exception as e:
    log.error( u'- in uc.sendFailureEmail(); SocketError is: %s; trying once more' % e )
    try:
      send_mail( subject, message, from_address, to_address_list, fail_silently=False )
      log.debug( u'- in uc.sendFailureEmail(); guess failure email was sent on second try' )
      return 'failure email sent'
    except Exception as f:
      log.error( u'- in uc.sendFailureEmail(); second Exception is: %s; returning' % f )
      return 'failure email failed'


def build_failure_email_message( name, check_frequency_number, check_frequency_unit, site_url, text_expected, email_message, admin_login_url ):
    """ Constructs failure message.
        Called by sendFailureEmail() """
    message = '''The service "%s" appears to be down.

The "%s" service failed two consecutive automated checks a few minutes apart. Checks will continue every few minutes while the failures persist, but you will only be emailed again when the automated check succeeds. Once the automated check succeeds, the check-frequency will return to the specified values of every-%s-%s(s).

- Url checked: "%s"
- Text expected: "%s"
- Specified failure message: "%s"

You can view the current status of all services set up for automated checking at:
<%s>

If authorized, you can edit service automated checking at:
<%s>

[end]
''' % ( name,
        name,
        check_frequency_number,
        check_frequency_unit,
        site_url,
        text_expected,
        email_message,
        '%s%s' % (settings_app.CHECKER_URL_ROOT, reverse('show_status_url')),
        '%s%s' % (settings_app.CHECKER_URL_ROOT, reverse('admin_login_url'))
        )
    log.debug( 'failure message, ```%s```' % message )
    return message


def sendPassedEmail( site ):
  '''
  - Purpose: sends back-online alert email
  - Called by: checkSites()
  '''
  try:
    from django.core.mail import send_mail
    subject = 'Service-Status alert: "%s" is ok now' % ( site.name, )
    message = build_passed_email_message( site.name, site.check_frequency_number, site.check_frequency_unit )
    from_address = settings_app.EMAIL_FROM_ADDRESS
    to_address_list = parseEmailAddresses( site.email_addresses )
    send_mail( subject, message, from_address, to_address_list, fail_silently=False )
    log.debug( u'- in uc.sendPassedEmail(); back-online email sent' )
    return 'back-online email sent'
  except Exception as e:
    log.error( u'- in uc.sendPassedEmail(); Exception is: %s; trying once more' % e )
    try:
      send_mail( subject, message, from_address, to_address_list, fail_silently=False )
      log.debug( u'- in uc.sendPassedEmail(); guess back-online email was sent on second try' )
      return 'back-online email sent'
    except Exception as f:
      log.error( u'- in uc.sendPassedEmail(); second Exception is: %s; returning' % f )
      return 'back-online email failed'

  # end def sendPassedEmail()


def build_passed_email_message( name, check_frequency_number, check_frequency_unit ):
    """ Constructs failure message.
        Called by sendPassedEmail() """
    message = '''The service "%s" appears to be up.

Automated checking will continue at the specified values of every-%s-%s(s).

You can view the current status of all services set up for automated checking at:
<%s>

If authorized, you can edit service automated checking at:
<%s>

[end]
''' % ( name,
        check_frequency_number,
        check_frequency_unit,
        '%s%s' % (settings_app.CHECKER_URL_ROOT, reverse('show_status_url')),
        '%s%s' % (settings_app.CHECKER_URL_ROOT, reverse('admin_login_url'))
        )
    log.debug( 'success message, ```%s```' % message )
    return message
