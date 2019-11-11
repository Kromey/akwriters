"""
Django settings for akwriters project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from . import site_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = site_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = site_settings.DEBUG

ADMINS = site_settings.ADMINS
SERVER_EMAIL = site_settings.SERVER_EMAIL
EMAIL_SUBJECT_PREFIX = '[AKWriters] '

ALLOWED_HOSTS = site_settings.ALLOWED_HOSTS


# Project templates
#TEMPLATE_DIRS = ( os.path.join(BASE_DIR, 'templates'), )
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'account',
    #'prosody',
    'alerts',
    'api',
    'chat',
    'contact',
    'events',
    'favicon',
    'helpers',
    'policies',
    'passwordless',
    'tools',
    'forum',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ROOT_URLCONF = 'akwriters.urls'

WSGI_APPLICATION = 'akwriters.wsgi.application'

# Nothing on our site should be allowed in any frames, not even our own
X_FRAME_OPTIONS = 'DENY'


# Authentication settings
LOGIN_URL = '/auth/login'
LOGOUT_URL = '/auth/logout'
AUTH_USER_MODEL = 'passwordless.User'

AUTHENTICATION_BACKENDS = (
    'passwordless.backend.TokenBackend',
    #'passwordless.backend.AppPasswordBackend',
)

SESSION_COOKIE_NAME = 'author'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_AGE = 7776000 # 90 days

CSRF_COOKIE_NAME = 'synopsis'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = site_settings.DATABASES

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Anchorage'

USE_I18N = True

USE_L10N = True

USE_TZ = True

GCAL_API_KEY = site_settings.GCAL_API_KEY
GAPI_CACHE_EXPIRES = site_settings.GAPI_CACHE_EXPIRES


# Custom settings
CONTACT_EMAIL = site_settings.CONTACT_EMAIL
JABBER_DOMAIN = site_settings.JABBER_DOMAIN
EMAIL_SENDER = site_settings.EMAIL_SENDER

NABU = site_settings.NABU

# Bot automatically added to new users' rosters
THE_BOT = site_settings.THE_BOT

# Override default message tags to fit with Bootstrap
from django.contrib.messages import constants as msg_constants
MESSAGE_TAGS = {
    msg_constants.ERROR: 'danger',
    msg_constants.DEBUG: 'warning',
    }
MESSAGE_LEVEL = site_settings.MESSAGE_LEVEL


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'site_assets'),
)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'htdocs/static')

