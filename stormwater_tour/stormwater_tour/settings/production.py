"""
Production settings for the stormwater_tour Django project.

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/
"""
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = False

X_FRAME_OPTIONS = 'DENY'

ALLOWED_HOSTS = [
    'localhost',
    '159.203.228.193'
]

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': PROD_DATABASE_PASS,
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_ROOT = '/home/django/stormwater_files/static/'

MEDIA_ROOT = '/home/django/stormwater_files/media/'

GOOGLE_MAP_API_KEY = TEST_PROD_GOOGLE_MAP_API_KEY
