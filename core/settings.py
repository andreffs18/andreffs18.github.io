# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# TEMPLATE_DIRS: set template path 
TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'core/templates'),)
# STATICFILE_DIRS: set static files path
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'core/static'),)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0%e(s#zxvz*t=3=$=$*6vky^po7#1qf&pg*br(&%5o)j)hg(!a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'


# Database Connection
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES={}
# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

import mongoengine
mongoengine.connect(os.environ.get("MONGO_DATABASE_NAME"), host=os.environ.get("MONGO_DATABASE_URL"))


# Logger configurations
LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': 'lineno=%(lineno)s funcname=%(funcName)s %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'root': {
            'handlers': ['console'],
            'level':'DEBUG'
    },
}

