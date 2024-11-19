"""
WSGI config.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import pathlib
import sys

from django.core.wsgi import get_wsgi_application

PROJECT_DIR_PATH = pathlib.Path(__file__).resolve().parent.parent
# print( f'PROJECT_DIR_PATH, ``{PROJECT_DIR_PATH}``' )

sys.path.append(str(PROJECT_DIR_PATH))

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'  # so django can access its settings

application = get_wsgi_application()


# #!/usr/bin/env python
# import os
# import sys

# if __name__ == '__main__':
#     print('hereAA')
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError:
#         # The above import may fail for some other reason. Ensure that the
#         # issue is really that Django is missing to avoid masking other
#         # exceptions on Python 2.
#         try:
#             import django
#         except ImportError:
#             raise ImportError(
#                 "Couldn't import Django. Are you sure it's installed and "
#                 'available on your PYTHONPATH environment variable? Did you '
#                 'forget to activate a virtual environment?'
#             )
#         raise
#     execute_from_command_line(sys.argv)
