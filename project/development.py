
# -*- coding: utf-8 -*-

from project.settings import *

SECRET_KEY = 'foo'

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    'LOCATION': 'velmu-test-cache',
    'TIMEOUT': 999999,
    'OPTIONS': {'MAX_ENTRIES': 99999999},
  }
}

#CACHES = {
#  'default': {
#    'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#    'LOCATION': os.path.join(BASEDIR, '..', 'django_cache'),
#    'TIMEOUT': 999999,
#    'OPTIONS': {'MAX_ENTRIES': 99999999},
#  }
#}

MIDDLEWARE_CLASSES += (
#  'debug_toolbar.middleware.DebugToolbarMiddleware',
)

AUTHENTICATION_BACKENDS = (
  'dreamsso.authbackend.local.SingleDatabaseBackend',
)

DEBUG_TOOLBAR_CONFIG = {
  'INTERCEPT_REDIRECTS': False,
}

INSTALLED_APPS += (
  #'django_extensions',
#  'debug_toolbar',
#  'django_nose',
)

DREAMSSO_USERDB_ENDPOINT = 'http://127.0.0.1:8002'
DREAM_APP_URL = 'http://localhost:8001'
DREAM_APP_HOSTNAME = 'localhost'

# Celery
BROKER_BACKEND = 'memory'
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_ALWAYS_EAGER = True

# Compress
COMPRESS_REBUILD_TIMEOUT = 0

# Testing
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SAUCELABS_USERNAME = ''
SAUCELABS_ACCESS_KEY = ''

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

