# -*- coding: utf-8 -*-

import os.path
import posixpath

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
LOCK_ROOT = os.path.join(PROJECT_ROOT, 'deploy', 'lock')
_ = lambda s: s

DEBUG = True

SITE_NAME = "SITE_NAME"
SITE_DOMAIN = '127.0.0.1:8000'

ADMINS = (
    ('frol', 'frolvlad@gmail.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = '@gmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

STATIC_URL = '/static/'

# Additional directories which hold static files
STATICFILES_DIRS = (
    ('project', os.path.join(PROJECT_ROOT, 'static')),
)
# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, 'admin/1/../')

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'FIX_IT'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
#    'auth_ext.middleware.LocaleMiddleware',

#    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'urls'

FIXTURE_DIRS = (
    'fixtures/',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
#    'misc.context_processors.useful_constants',
)

INSTALLED_APPS = (
# Django internal modules
	
# Admin part
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',

# Standart modules
    'south',
    'coffin',
    'bootstrap3',
    'bootstrap3_ext',

# Escalibro's modules
#    'misc',

# Local modules
    'auth_ext',
    'fling_receiver',
)

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_REQUIRED_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = False
EMAIL_CONFIRMATION_DAYS = 14
LOGIN_REDIRECT_URL = LOGIN_REDIRECT_URLNAME = 'root'
LOGOUT_REDIRECT_URLNAME = 'root'
LOGOUT_URL = '/auth/logout/'
LOGIN_URL = '/auth/login/'
SESSION_MAX_AGE = 60 * 60 * 24 * 7 * 2 # 2 weeks

LANGUAGES = (
    ('en', u'English'),
    ('ru', u'Russian'),
)

#PAGINATION_INVALID_PAGE_RAISES_404 = True
#PAGINATION_DEFAULT_PAGINATION = 10

AUTH_USER_MODEL = 'auth_ext.User'


# Logging
TIMELOG_LOG = 'deploy/var/log/timelog.log'
CONSOLE_LOG = 'deploy/var/log/console.log'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'plain': {
            'format': '%(asctime)s %(message)s'
        },
    },
    'handlers': {
        'timelog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': TIMELOG_LOG,
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'plain',
        },
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'file':{
            'level':'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': CONSOLE_LOG,
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 20,
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': [],
        }
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {
            #'handlers': ['mail_admins'],
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'distributed_queue': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}


try:
    from local_settings import *
except ImportError:
    pass

SERVE_MEDIA = DEBUG
