"""
Django settings for akwriters project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#Found in site_settings.py

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['akwriters.org']


# Project templates
TEMPLATE_DIRS = ( os.path.join(BASE_DIR, 'templates'), )


# Application definition

INSTALLED_APPS = (
    #'django.contrib.admin',
    #'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'alerts',
    'api',
    'chat',
    'contact',
    'favicon',
    'helpers',
    'policies',
    'prosodyauth',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'prosodyauth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'akwriters.urls'

WSGI_APPLICATION = 'akwriters.wsgi.application'


# Authentication settings
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

AUTHENTICATION_BACKENDS = (
    'backends.prosody.ProsodyBackend',
)


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
#Set in site_settings

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Anchorage'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Custom settings
PROSODY_DEFAULT_DOMAIN = 'akwriters.org'
EMAIL_SENDER = 'Alaska Writers <prosody@akwriters.org>'

#Number of iterations for SCRAM password hashing
SCRAM_ITERATIONS = 8192

# Bot automatically added to new users' rosters
THE_BOT = {
    'name': 'Annika',
    'jid': 'annika@akwriters.org',
}

# Override default message tags to fit with Bootstrap
from django.contrib.messages import constants as msg_constants
MESSAGE_TAGS = {
    msg_constants.ERROR: 'danger',
    msg_constants.DEBUG: 'warning',
    }


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '//static.akwriters.org/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "htdocs/static"),
)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
STATIC_ROOT = '/var/www/akwriters.org/static'

#This should be the very last line, always, so we can override anything in
#settings.py with site- or environment-specific values.
from .site_settings import *
