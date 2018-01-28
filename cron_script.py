# -*- coding: utf-8 -*-

"""
Determines which sites are ready to be checked, and checks them
Called by: crontab
"""

import datetime, logging, os
import django

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
    return


if __name__ == "__main__":
    run_code()
