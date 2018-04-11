
# -*- coding: utf-8 -*-

import os
import logging

BASEDIR = os.path.dirname(os.path.abspath(__file__))

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

INTERNAL_IPS = ('127.0.0.1',)

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASEDIR, 'database.db'),
  }
}

CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
  }
}

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_NAME = 'appsid'
SESSION_COOKIE_AGE = 60 * 60

SITE_ID = 1

USE_TZ = True
TIME_ZONE = 'Europe/Helsinki'

LANGUAGE_CODE = 'fi'

LANGUAGES = (
    ('en', 'EN'),
    ('fi', 'FI'),
    ('sv', 'SV'),
)

LOCALE_PATHS = (
  os.path.join(BASEDIR, 'locale'),
)

LOGIN_URL = '/login/mpass/'
LOGIN_REDIRECT_URL = '/'

STATICFILES_DIRS = (
  os.path.join(BASEDIR, 'static'),
)

STATIC_ROOT = os.path.join(BASEDIR, '..', 'staticroot')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASEDIR, '..', 'mediaroot')

MEDIA_URL = '/media/'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'dreamsso.middleware.OrganisationSelectMiddleware',
    'dreamsso.middleware.LocaleMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'hutils.middleware.MinifyHtmlMiddleware',
    'velmu.middleware.MethodOverrideMiddleware',
#    'django.middleware.gzip.GZipMiddleware',
)

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
  {
    'BACKEND':'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASEDIR, 'templates')],
    'OPTIONS': {
      'loaders': [
        'apptemplates.Loader',
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
      ],
      'context_processors': [
        'django.contrib.auth.context_processors.auth',
        'django.template.context_processors.debug',
        'django.template.context_processors.i18n',
        'django.template.context_processors.media',
        'django.template.context_processors.static',
        'django.contrib.messages.context_processors.messages',
        'django.template.context_processors.request',
      ],
    }
  },
]

STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
  'compressor.finders.CompressorFinder',
)

INSTALLED_APPS = (
    'velmu',
    'dreamcards',
    'dreamsso',
    'dreamuserdb',
    'mpass',

    'compressor',
    'mptt',
    'parler',
    'rest_framework',

    'health_check',
    'health_check_celery3',
    'health_check_db',
    'health_check_cache',
    'health_check_storage',
    'hutils.health_check_sentry',

    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'django.contrib.admin.apps.SimpleAdminConfig',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
      'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
      'rest_framework.filters.SearchFilter',
    ),
    'DEFAULT_RENDERER_CLASSES': (
      'rest_framework.renderers.JSONRenderer',
      # TODO: We might want to remove BrowsableAPI in production eventually
      'rest_framework.renderers.BrowsableAPIRenderer',
    )
}

# Compress
COMPRESS_HTML = False
COMPRESS_PARSER = 'compressor.parser.HtmlParser'
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False
COMPRESS_CSS_FILTERS = [
  'compressor.filters.css_default.CssAbsoluteFilter',
  'hutils.compressor_filters.ScssFilter',
]

# Workaround for pyScss problems
# https://github.com/Kronuz/pyScss/issues/70
logging.getLogger('scss').addHandler(logging.StreamHandler())

DREAMCARDS_CARD_THUMBNAIL_WIDTH = 150
DREAMCARDS_CARD_THUMBNAIL_HEIGHT = 125
DREAMCARDS_CARD_SERIALIZERS = {}

DREAMUSERDB_DOMAIN = 'http://localhost:8000'
DREAMUSERDB_CHECK_USERNAME_FORMAT = False
DREAMSSO_USER_PTR_RELATED_NAME = 'dreamsso_user'
DREAM_APP_URL = 'https://demo.velmu.fi'
DREAM_APP_HOSTNAME = 'demo.velmu.fi'
VELMU_APP_URL = DREAM_APP_URL

MPASS_IDP_URL = 'https://mpass-proxy-test.csc.fi'

PARLER_LANGUAGES = {
    None: (
        {'code': 'fi',},
        {'code': 'sv',},
    ),
    'default': {
        'fallbacks': ['fi'],          # defaults to PARLER_DEFAULT_LANGUAGE_CODE
        'hide_untranslated': False,   # the default; let .active_translations() return fallbacks too.
    }
}

CELERY_TASK_PROTOCOL = 1  # fixes problems with queuing tasks from celery beat
CELERY_BEAT_SCHEDULE = {
  'mpass-sync-auth-sources': {
    'task': 'mpass.tasks.fetch_mpass_authentication_sources',
    'schedule': 5*60,  # every 5 minutes
  },
  'mpass-sync-services': {
    'task': 'mpass.tasks.fetch_mpass_services',
    'schedule': 5*60,  # every 5 minutes
  },
}


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

