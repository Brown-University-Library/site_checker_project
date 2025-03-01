# -*- coding: utf-8 -*-

import json
import logging
import pprint

from django.conf import settings as project_settings
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from . import settings_app
from .lib import version_helper
from .lib.shib_auth import shib_login  # decorator
from .models import CheckSite

log = logging.getLogger(__name__)


def show_status(request):
    """Displays public status page."""
    site_data = CheckSite.objects.all().order_by('name')
    context = {'object_list': site_data}
    return render(request, 'site_checker_app_templates/checksite_list.html', context)


def show_status_old(request):
    """Displays public status page."""
    site_data = CheckSite.objects.all().order_by('name')
    context = {'object_list': site_data}
    return render(request, 'site_checker_app_templates/checksite_list_old.html', context)


@shib_login
def login(request):
    """Handles shib authNZ & redirects to admin."""
    admin_url = reverse('admin:site_checker_app_checksite_changelist')
    log.debug('admin_url, ```%s```' % admin_url)
    return HttpResponseRedirect(admin_url)


def bul_search(request):
    """Triggered by user entering search term into banner-search-field.
    Redirects query to search.library.brown.edu"""
    log.debug('request.__dict__, ```%s```' % pprint.pformat(request.__dict__))
    redirect_url = 'https://search.library.brown.edu?%s' % request.META['QUERY_STRING']
    return HttpResponseRedirect(redirect_url)


# ===========================
# for development convenience
# ===========================


def info(request):
    """Returns basic info.
    Getting this running shows that logging is working, and that the settings_app file is properly reading env-vars."""
    log.debug('request.__dict__, ```%s```' % pprint.pformat(request.__dict__))
    # start = datetime.datetime.now()
    # start = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
    start = timezone.now()
    commit = version_helper.get_commit()
    branch = version_helper.get_branch()
    info_txt = commit.replace('commit', branch)
    rtrn_dct = {
        'query': {
            'date_time': str(start),
            'url': '{schm}://{hst}{uri}'.format(
                schm=request.scheme,
                hst=request.headers['host'],
                uri=request.META.get('REQUEST_URI', request.META['PATH_INFO']),
            ),
        },  # REQUEST_URI not available via run-server
        'response': {
            'documentation': settings_app.README_URL,
            # 'elapsed_time': str(datetime.datetime.now() - start),
            'elapsed_time': str(timezone.now() - start),
            'version': info_txt,
        },
    }
    return HttpResponse(json.dumps(rtrn_dct, sort_keys=True, indent=2), content_type='application/javascript; charset=utf-8')


def error_check(request):
    """For checking that admins receive error-emails."""
    if project_settings.DEBUG:
        raise Exception('testing error-email')
    else:
        return HttpResponseNotFound('<div>404 / Not Found</div>')
