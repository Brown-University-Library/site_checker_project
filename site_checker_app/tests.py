# -*- coding: utf-8 -*-

import datetime
import logging

from django.test import TestCase

from . import settings_app
from .lib import utility_code
from .models import CheckSite

log = logging.getLogger(__name__)
TestCase.maxDiff = None


class RootUrlTest(TestCase):
    """Checks root urls."""

    def test_root_url_no_slash(self):
        """Checks '/root_url'."""
        response = self.client.get('')  # project root part of url is assumed
        self.assertEqual(302, response.status_code)  # non-permanent redirect
        redirect_url = response._headers['location'][1]
        self.assertEqual('/status/', redirect_url)

    def test_root_url_slash(self):
        """Checks '/root_url/'."""
        response = self.client.get('/')  # project root part of url is assumed
        self.assertEqual(302, response.status_code)  # permanent redirect
        redirect_url = response._headers['location'][1]
        self.assertEqual('/status/', redirect_url)

    # end class RootUrlTest()


class UtilityCodeTests(TestCase):
    """Checks lib.utility_code.py functions.
    TODO: refactor functions into appropriate modules/classes where applicable, and update tests."""

    ## checkSite()

    def test_checkSite_funkyPdf(self):
        ## make site
        s = CheckSite()
        s.name = 'abc123_test-page.title'
        s.url = settings_app.TEST_SITE_URL_TO_FUNKY_PDF  # reading this PDF throws unicode error
        s.text_expected = 'BleedBox'  # it's there
        s.check_frequency_number = 1
        s.check_frequency_unit = 'minute'
        s.email_addresses = settings_app.TEST_EMAIL
        s.email_message = 'not_applicable'
        s.recent_checked_time = datetime.datetime(2007, 1, 15)  # 2007-01-15, 00:00am
        ## check site
        utility_code.checkSiteV2(s)
        # expected = 'passed_though_non_unicode'
        expected = 'passed'
        result = s.recent_checked_result
        self.assertTrue(
            expected == result,
            '\n Expected: ->%s<-; \nresult is: ->%s<-'
            % (
                expected,
                result,
            ),
        )

    def test_checkSite_siteExistsGoodHtml(self):
        ## make site
        s = CheckSite()
        s.name = 'abc123_test-page.title'
        s.url = settings_app.TEST_SITE_URL_GOOD_HTML  # page exists, with expected text
        log.debug('s.url, ``%s``' % s.url)
        s.text_expected = 'Skip to events'
        s.check_frequency_number = 1
        s.check_frequency_unit = 'minute'
        s.email_addresses = settings_app.TEST_EMAIL
        s.email_message = 'problem with test-page'
        s.recent_checked_time = datetime.datetime(2007, 1, 15)  # 2007-01-15, 00:00am
        ## check site
        utility_code.checkSiteV2(s)
        expected = 'passed'
        result = s.recent_checked_result
        log.debug('result, ``%s``' % result)
        self.assertTrue(
            expected == result,
            '\n Expected: ->%s<-; \nresult is: ->%s<-'
            % (
                expected,
                result,
            ),
        )

    def test_checkSite_textNotFound(self):
        ## make site
        s = CheckSite()
        s.name = 'abc123_test-page.title'
        s.url = settings_app.TEST_SITE_URL_GOOD_HTML  # page exists
        s.text_expected = '<title>blahblah</title>'  # won't be found
        s.check_frequency_number = 1
        s.check_frequency_unit = 'minute'
        s.email_addresses = settings_app.TEST_EMAIL
        s.email_message = 'problem with test-page'
        s.recent_checked_time = datetime.datetime(2007, 1, 15)  # 2007-01-15, 00:00am
        ## check site
        utility_code.checkSiteV2(s)
        expected = 'text_not_found'
        result = s.recent_checked_result
        self.assertTrue(
            expected == result,
            '\n Expected: ->%s<-; \nresult is: ->%s<-'
            % (
                expected,
                result,
            ),
        )

    # def test_checkSite_urlNotAccessible(self):
    #   '''
    #   TODO: use ability of urllib2 to return a 404 indicator
    #   '''
    #   # end def test_checkSite_urlNotAccessible()

    # def test_checkSite_responseTakingTooLong(self):
    #   '''
    #   TODO: first improvement priority, because this issue can result in multiple emails sent
    #         Research and use the socket-timeout approach.
    #   '''
    #   # end def test_checkSite_responseTakingTooLong()

    ## grabSitesToCheck()

    def test_grabSitesToCheck_noRetrieval(self):
        ## make site that should *not* be retrieved
        s = CheckSite()
        # irrelevant for test...
        s.name = 'abc123_test-page.title'
        s.url = settings_app.TEST_SITE_URL_GOOD_HTML
        s.text_expected = '<title>blahblah</title>'
        s.email_addresses = settings_app.TEST_EMAIL
        s.email_message = 'problem with test-page'
        # relevant for test...
        s.recent_checked_time = datetime.datetime(2007, 1, 15)  # 2007-01-15, 00:00am
        s.check_frequency_number = 10
        s.check_frequency_unit = 'minute'
        s.recent_checked_result = 'passed'  # so that time_delta is calculated normally
        s.save()  # s.next_check_time is auto-calculated to be 10 minutes later
        ## test
        test_datetime = datetime.datetime(
            2007, 1, 15, 0, 5
        )  # 2007-01-15 00:05am; so should not be checked, because it's been only 5 minutes since last check
        query_set = utility_code.grabSitesToCheck(test_datetime)['query_set']
        expected = 0
        result = query_set.count()
        self.assertTrue(
            expected == result,
            '\n Expected: ->%s<-; \nresult is: ->%s<-'
            % (
                expected,
                result,
            ),
        )

    def test_grabSitesToCheck_retrieval(self):
        ## make site that should *not* be retrieved
        s = CheckSite()
        # irrelevant for test...
        s.name = 'abc123_test-page.title'
        s.url = settings_app.TEST_SITE_URL_GOOD_HTML
        s.text_expected = '<title>blahblah</title>'
        s.email_addresses = settings_app.TEST_EMAIL
        s.email_message = 'problem with test-page'
        # relevant for test...
        s.recent_checked_time = datetime.datetime(2007, 1, 15)  # 2007-01-15, 00:00am
        s.check_frequency_number = 10
        s.check_frequency_unit = 'minute'
        s.recent_checked_result = 'passed'  # so that time_delta is calculated normally
        s.save()  # s.next_check_time is auto-calculated to be 10 minutes later
        ## test
        test_datetime = datetime.datetime(
            2007, 1, 15, 0, 12
        )  # 2007-01-15 00:12am; so should be checked, because it's been more than 10 minutes
        query_set = utility_code.grabSitesToCheck(test_datetime)['query_set']
        expected = 1
        result = query_set.count()
        self.assertTrue(
            expected == result,
            '\n Expected: ->%s<-; \nresult is: ->%s<-'
            % (
                expected,
                result,
            ),
        )

    ## parseEmailAddresses()

    def test_parseEmailAddresses_single(self):
        field_string = 'aaa@test.com'
        expected = ['aaa@test.com']
        result = utility_code.parseEmailAddresses(field_string)
        self.assertTrue(
            expected == result,
            '\n Expected: ->%s<-; \nresult is: ->%s<-'
            % (
                expected,
                result,
            ),
        )

    def test_parseEmailAddresses_multipleViaComma(self):
        field_string = 'aaa@test.com,bbb@test.com'
        expected = ['aaa@test.com', 'bbb@test.com']
        result = utility_code.parseEmailAddresses(field_string)
        self.assertTrue(
            expected == result,
            '\n Expected: ->%s<-; \nresult is: ->%s<-'
            % (
                expected,
                result,
            ),
        )

    def test_parseEmailAddresses_multipleViaCommaAndSpace(self):
        field_string = 'aaa@test.com, bbb@test.com'
        expected = ['aaa@test.com', 'bbb@test.com']
        result = utility_code.parseEmailAddresses(field_string)
        self.assertTrue(
            expected == result,
            '\n Expected: ->%s<-; \nresult is: ->%s<-'
            % (
                expected,
                result,
            ),
        )

    ## runEmailCheck()

    def test_runEmailCheck_failureEmailAfterTwoFailures(self):
        ## make site
        s = CheckSite()
        s.name = 'abc123_test-page.title'
        s.url = 'irrelevant'  # checkSite() not being called
        s.text_expected = 'irrelevant'
        s.check_frequency_number = 1
        s.check_frequency_unit = 'minute'
        s.email_addresses = settings_app.TEST_EMAIL
        s.email_message = 'irrelevant -- but it would be some kind of "success" message'
        s.recent_checked_time = datetime.datetime(2007, 1, 15)  # 2007-01-15, 00:00am
        s.recent_checked_result = 'url_not_accessible'  # would be set from calling 'checkSite()'; this and following two statuses are what's being used to determine def response
        s.previous_checked_result = 'url_not_accessible'
        s.pre_previous_checked_result = 'passed'
        ## run check
        expected = 'send_failure_email'
        result = utility_code.runEmailCheck(s)
        self.assertTrue(
            expected == result,
            '\n Expected: ->%s<-; \nresult is: ->%s<-'
            % (
                expected,
                result,
            ),
        )

    def test_runEmailCheck_failureEmailSoonAfterCreation(self):
        ## make site
        s = CheckSite()
        s.name = 'abc123_test-page.title'
        s.url = 'irrelevant'  # checkSite() not being called
        s.text_expected = 'irrelevant'
        s.check_frequency_number = 1
        s.check_frequency_unit = 'minute'
        s.email_addresses = settings_app.TEST_EMAIL
        s.email_message = 'irrelevant -- but it would be some kind of "failure" message'
        s.recent_checked_time = datetime.datetime(2007, 1, 15)  # 2007-01-15, 00:00am
        s.recent_checked_result = 'text_not_found'  # would be set from calling 'checkSite()'; this and following two statuses are what's being used to determine def response
        s.previous_checked_result = 'text_not_found'
        s.pre_previous_checked_result = 'init'
        ## run check
        expected = 'send_failure_email'
        result = utility_code.runEmailCheck(s)
        self.assertTrue(
            expected == result,
            '\n Expected: ->%s<-; \nresult is: ->%s<-'
            % (
                expected,
                result,
            ),
        )

    def test_runEmailCheck_noEmailNewCreation(self):
        """
        I don't think this would ever get called,
        since checkSite() would update the virgin record, but can't hurt to have in.
        """
        ## make site
        s = CheckSite()
        s.name = 'abc123_test-page.title'
        s.url = 'irrelevant'  # checkSite() not being called
        s.text_expected = 'irrelevant'
        s.check_frequency_number = 1
        s.check_frequency_unit = 'minute'
        s.email_addresses = settings_app.TEST_EMAIL
        s.email_message = 'irrelevant -- but it would be some kind of "failure" message'
        s.recent_checked_time = datetime.datetime(2007, 1, 15)  # 2007-01-15, 00:00am
        s.recent_checked_result = 'init'  # would be set from calling 'checkSite()'; this and following two statuses are what's being used to determine def response
        s.previous_checked_result = 'init'
        s.pre_previous_checked_result = 'init'
        ## run check
        expected = 'send_no_email'
        result = utility_code.runEmailCheck(s)
        self.assertTrue(
            expected == result,
            '\n Expected: ->%s<-; \nresult is: ->%s<-'
            % (
                expected,
                result,
            ),
        )

    def test_runEmailCheck_noEmailOnRepeatedFailure(self):
        ## make site
        s = CheckSite()
        s.name = 'abc123_test-page.title'
        s.url = 'irrelevant'  # checkSite() not being called
        s.text_expected = 'irrelevant'
        s.check_frequency_number = 1
        s.check_frequency_unit = 'minute'
        s.email_addresses = settings_app.TEST_EMAIL
        s.email_message = 'irrelevant -- but it would be some kind of "success" message'
        s.recent_checked_time = datetime.datetime(2007, 1, 15)  # 2007-01-15, 00:00am
        s.recent_checked_result = 'url_not_accessible'  # would be set from calling 'checkSite()'; this and following two statuses are what's being used to determine def response
        s.previous_checked_result = 'url_not_accessible'
        s.pre_previous_checked_result = 'url_not_accessible'
        ## run check
        expected = 'send_no_email'
        result = utility_code.runEmailCheck(s)
        self.assertTrue(
            expected == result,
            '\n Expected: ->%s<-; \nresult is: ->%s<-'
            % (
                expected,
                result,
            ),
        )

    def test_runEmailCheck_noEmailOnSinglePastFailureWithCurrentSuccess(self):
        ## make site
        s = CheckSite()
        s.name = 'abc123_test-page.title'
        s.url = 'irrelevant'  # checkSite() not being called
        s.text_expected = 'irrelevant'
        s.check_frequency_number = 1
        s.check_frequency_unit = 'minute'
        s.email_addresses = settings_app.TEST_EMAIL
        s.email_message = 'irrelevant -- but it would be some kind of "success" message'
        s.recent_checked_time = datetime.datetime(2007, 1, 15)  # 2007-01-15, 00:00am
        s.recent_checked_result = 'passed'  # would be set from calling 'checkSite()'; this and following two statuses are what's being used to determine def response
        s.previous_checked_result = 'url_not_accessible'
        s.pre_previous_checked_result = 'passed'
        ## run check
        expected = 'send_no_email'
        result = utility_code.runEmailCheck(s)
        self.assertTrue(
            expected == result,
            '\n Expected: ->%s<-; \nresult is: ->%s<-'
            % (
                expected,
                result,
            ),
        )

    def test_runEmailCheck_noEmailOnRepeatedSuccess(self):
        ## make site
        s = CheckSite()
        s.name = 'abc123_test-page.title'
        s.url = 'irrelevant'  # checkSite() not being called
        s.text_expected = 'irrelevant'
        s.check_frequency_number = 1
        s.check_frequency_unit = 'minute'
        s.email_addresses = settings_app.TEST_EMAIL
        s.email_message = 'irrelevant -- but it would be some kind of "success" message'
        s.recent_checked_time = datetime.datetime(2007, 1, 15)  # 2007-01-15, 00:00am
        s.recent_checked_result = 'passed'  # would be set from calling 'checkSite()'; this and following two statuses are what's being used to determine def response
        s.previous_checked_result = 'passed'
        s.pre_previous_checked_result = 'passed'
        ## run check
        expected = 'send_no_email'
        result = utility_code.runEmailCheck(s)
        self.assertTrue(
            expected == result,
            '\n Expected: ->%s<-; \nresult is: ->%s<-'
            % (
                expected,
                result,
            ),
        )

    def test_runEmailCheck_noEmailRightAfterCreation(self):
        ## make site
        s = CheckSite()
        s.name = 'abc123_test-page.title'
        s.url = 'irrelevant'  # checkSite() not being called
        s.text_expected = 'irrelevant'
        s.check_frequency_number = 1
        s.check_frequency_unit = 'minute'
        s.email_addresses = settings_app.TEST_EMAIL
        s.email_message = 'irrelevant -- but it would be some kind of "failure" message'
        s.recent_checked_time = datetime.datetime(2007, 1, 15)  # 2007-01-15, 00:00am
        s.recent_checked_result = 'text_not_found'  # would be set from calling 'checkSite()'; this and following two statuses are what's being used to determine def response
        s.previous_checked_result = 'init'
        s.pre_previous_checked_result = 'init'
        ## run check
        expected = 'send_no_email'
        result = utility_code.runEmailCheck(s)
        self.assertTrue(
            expected == result,
            '\n Expected: ->%s<-; \nresult is: ->%s<-'
            % (
                expected,
                result,
            ),
        )

    def test_runEmailCheck_successEmailAfterFailures(self):
        ## make site
        s = CheckSite()
        s.name = 'abc123_test-page.title'
        s.url = 'irrelevant'  # checkSite() not being called
        s.text_expected = 'irrelevant'
        s.check_frequency_number = 1
        s.check_frequency_unit = 'minute'
        s.email_addresses = settings_app.TEST_EMAIL
        s.email_message = 'irrelevant -- but it would be some kind of "success" message'
        s.recent_checked_time = datetime.datetime(2007, 1, 15)  # 2007-01-15, 00:00am
        s.recent_checked_result = 'passed'  # would be set from calling 'checkSite()'; this and following two statuses are what's being used to determine def response
        s.previous_checked_result = 'url_not_accessible'
        s.pre_previous_checked_result = 'url_not_accessible'
        ## run check
        expected = 'send_success_email'
        result = utility_code.runEmailCheck(s)
        self.assertTrue(
            expected == result,
            '\n Expected: ->%s<-; \nresult is: ->%s<-'
            % (
                expected,
                result,
            ),
        )


## end class UtilityCodeTests()
