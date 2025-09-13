# WSGI configuration for PythonAnywhere
# Django web application configuration

import os
import sys

# Add your project directory to the Python path
path = '/home/webcraft/mysite'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'webbuilder.settings_production'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
