import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = int(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", '').split(" ")
# ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps
    'rest_framework',

    # local apps
    'common',
    'users',
    'userconfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'base.wsgi.application'


# Database

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
        "NAME": os.environ.get("SQL_DATABASE", "db.sqlite3"),
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.CustomUser'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/login/'

AUTHENTICATION_BACKENDS = [
    'common.models.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]


# Logging


LOGS_DIR = os.path.join(BASE_DIR, 'logs')

LOGGING_BACKUP_COUNT = 10
LOGGING_MAX_BYTES = 1024 * 1024 * 5  # 1024*1024 bytes (1MB)


def format_long_path(record):
    if str(BASE_DIR) in str(record.pathname):
        record.pathname = record.pathname.replace(str(BASE_DIR), '').replace(os.sep, '.')

    if record.pathname.startswith('.'):
        record.pathname = record.pathname[1:]

    return True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} | {pathname}.{funcName}(), Ln {lineno}: {message}',
            'style': '{',
        },
    },
    'filters': {
        'format_path': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': format_long_path,
        },
    },
    'handlers': {
        'file_info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'info.log'),
            'formatter': 'verbose',
            'filters': ['format_path'],
            'backupCount': LOGGING_BACKUP_COUNT,
            'maxBytes': LOGGING_MAX_BYTES,
            'delay': True,
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'debug.log'),
            'formatter': 'verbose',
            'filters': ['format_path'],
            'backupCount': LOGGING_BACKUP_COUNT,
            'maxBytes': LOGGING_MAX_BYTES,
            'delay': True,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file_info'],
            'propagate': True,
        },
        'debug': {
            'handlers': ['file_debug'],
            'propagate': True,
        },
    }
}
