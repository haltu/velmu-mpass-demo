
# -*- coding: utf-8 -*-

#- This file documents what are the settings needed in production
#- The values should not be written here, just documentation what
#- is needed.
#-
#- Infrastructure specific settings in production come from local_settings.py
#- which is importing this file.

from project.settings import *

DEBUG = False
TEMPLATE_DEBUG = False

MAINTENANCE_MODE = False

# Get from salt
SECRET_KEY = ''

INTERNAL_IPS = (
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SENTRY_SITE = 'app'


# wrap template loaders inside cached loader
TEMPLATES[0]['OPTIONS']['loaders'] = [('django.template.loaders.cached.Loader', TEMPLATES[0]['OPTIONS']['loaders'])]

DREAM_APP_URL = 'https://velmu.fi'
DREAM_APP_HOSTNAME = 'velmu.fi'

# Compress
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_HTML = True
# Address celery problems (task #5540)
BROKER_HEARTBEAT = 0

AUTHENTICATION_BACKENDS = (
  'velmu.authbackends.MPASSBackend',
  'dreamsso.authbackend.local.SingleDatabaseBackend',
)

# Sentry
SENTRY_DSN = ''
SENTRY_SITE = ''

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

