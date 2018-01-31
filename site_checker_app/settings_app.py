# -*- coding: utf-8 -*-

import json, os


README_URL = os.environ['SITECHKR__README_URL']

DEFAULT_RECHECK_MINUTES = int( os.environ['SITECHKR__DEFAULT_RECHECK_MINUTES'] )

EMAIL_FROM_ADDRESS = os.environ['SITECHKR__EMAIL_FROM_ADDRESS']

CHECKER_URL_ROOT = os.environ['SITECHKR__URL_ROOT']

STAFF_GROUP = os.environ['SITECHKR__STAFF_GROUP']

## for shib-auth
TEST_META_DCT = json.loads( os.environ['SITECHKR__TEST_META_DCT_JSON'] )  # for local devbox development
SUPER_USERS = json.loads( os.environ['SITECHKR__SUPER_USERS_JSON'] )

## just for tests
TEST_EMAIL = os.environ['SITECHKR__TEST_EMAIL']
TEST_SITE_URL_GOOD_HTML = os.environ['SITECHKR__TEST_SITE_URL_GOOD_HTML']
TEST_SITE_URL_TO_FUNKY_PDF = os.environ['SITECHKR__TEST_SITE_URL_TO_FUNKY_PDF']
