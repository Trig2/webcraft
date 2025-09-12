"""
Production settings for PythonAnywhere deployment
IMPORTANT: Replace 'yourusername' with your actual PythonAnywhere username
"""

import os
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# IMPORTANT: Replace 'yourusername' with your actual PythonAnywhere username
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']

# Database - keeping SQLite for easier deployment
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/yourusername/DjangoProject/db.sqlite3',
    }
}

# Static files configuration for production
STATIC_URL = '/static/'
STATIC_ROOT = '/home/yourusername/DjangoProject/staticfiles'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/yourusername/DjangoProject/media'

# Remove development-only apps from INSTALLED_APPS
INSTALLED_APPS = [
    app for app in INSTALLED_APPS 
    if app not in [
        'tailwind', 
        'theme', 
        'channels',
        'django_browser_reload'  # Remove browser reload app
    ]
]
CHANNEL_LAYERS = {}

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Use environment variable for secret key if available
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

# Simplified logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/home/yourusername/DjangoProject/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
