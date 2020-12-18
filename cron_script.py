# -*- coding: utf-8 -*-

"""
Determines which sites are ready to be checked, and checks them
Called by: crontab

Suggested calling mechanism from crontab...

## (crontab reminder: MINUTE HOUR DAYOFMONTH MONTH DAYOFWEEK COMMAND)
* * * * * cd /path/to/site_checker_project/; source ../venv/bin/activate > /dev/null; ../venv/bin/python3 ./cron_script.py

"""

import datetime, logging, os, time
import django
from django import db

## set up django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

## now django imports will work
from site_checker_app.lib import utility_code


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s', datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger(__name__)


def run_code():
    """ Calls site-checker code. """
    log.debug( 'starting check' )
    now_time = datetime.datetime.now()
    sites_to_check = utility_code.grabSitesToCheck( now_time )['query_set']
    utility_code.checkSites( sites_to_check )
    db.close_old_connections()
    time.sleep( .5 )
    return


if __name__ == "__main__":
    run_code()
