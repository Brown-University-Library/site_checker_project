# -*- coding: utf-8 -*-


'''
- Purpose: determines which sites are ready to be checked, and checks them
- Called by: crontab
'''


def runCode():

  try:
    ## setup environment
    paths_set = updateSysPaths()
    import datetime, os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'services.settings'
    from site_check_app import settings_app, utility_code
    execfile( settings_app.ACTIVATE_FILE, dict(__file__=settings_app.ACTIVATE_FILE) )  # so requests module can be accessed

    ## work
    nowtime = datetime.datetime.now()
    utility_code.updateLog( u'- in cron_script.py; starting script at: %s' % str( nowtime ), message_importance='high' )
    sites_to_check = utility_code.grabSitesToCheck( nowtime )['query_set']
    utility_code.checkSites( sites_to_check )
    endtime = datetime.datetime.now()
    utility_code.updateLog( u'- in cron_script.py; ending script at: %s; time-taken: %s' % ( str(endtime), str(endtime - nowtime) ), message_importance='high' )
  except:
    message = u'- in cron_script.py; exception info: %s' % utility_code.makeErrorString()
    utility_code.updateLog( message, message_importance='high' )
    print message


def updateSysPaths():
  '''
  - Purpose: append project-directory, and its enclosing directory to the python path
  - Called by: runCode()
  '''
  try:
    import os, sys
    ## get project's enclosing directory
    current_script_name = sys.argv[0]   # might be a full path, depending how script was called, but might only be: eg './sample_script.py'
    project_directory_path = os.path.dirname( current_script_name )   # eg '.'
    full_project_directory_path = os.path.abspath( project_directory_path )   # eg '/path/to/sample_project'
    directory_list = full_project_directory_path.split('/')   # eg ['', 'Users', 'username', 'Desktop', 'sample_project', 'sample_app']
    project_directory_name = directory_list[-2]   # eg 'sample_project'
    cut_position_start = full_project_directory_path.find( '/' + project_directory_name )
    cut_segment = full_project_directory_path[ cut_position_start:]
    directory_enclosing_project_directory_path = full_project_directory_path.replace( cut_segment, '' )  # eg '/path/to/sample_project'
    project_directory_path = '%s/%s' % (directory_enclosing_project_directory_path, project_directory_name)
    sys.path.append( directory_enclosing_project_directory_path )
    sys.path.append( project_directory_path )
    return {'status': 'paths_set', 'sys-path': sys.path }
  except Exception, e:
    print u'- in cron_script.py; problem appending sys.path; exception is: %s' % e



if __name__ == "__main__":
  runCode()
