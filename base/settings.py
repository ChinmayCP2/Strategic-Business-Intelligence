"""
Django settings for base project.

Generated by 'django-admin startproject' using Django 4.2.14.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)w$i4!ocujkx!sj4p0yd07_+%&y7d)huupmiwg1513h@n)=j%j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lgd',
    'strategicbi',
    'auth_app',
    'crispy_bootstrap5',
    'crispy_forms',
    "debug_toolbar",
    'django_celery_results',
]

CRISPY_ALLOWED_TEMPLETES_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lgd',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

SESSION_EXPIRE_SECONDS = 1800
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_TIMEOUT_REDIRECT = "/login/"

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
# STATICFILES_DIRS = [ BASE_DIR / 'static']
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = "/bi/fetch/"
LOGOUT_REDIRECT_URL = "/login/"

CRISPY_FORMS_SETTINGS = {
    'form_show_errors' : True
}
INTERNAL_IPS = [
    "127.0.0.1",
]
DEBUG_TOOLBAR_CONFIG = {
    'RECORD_REDIRECTS': True,
}

LOGGING = {
   'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{asctime} - {levelname} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'auth_app': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'auth_app.log',
            'formatter': 'simple',
        },
        'strategicbi': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'strategicbi.log',
            'formatter': 'simple',
        },
        'lgd': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'lgd.log',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'auth_app': {
            'handlers': ['auth_app'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'strategicbi': {
            'handlers': ['strategicbi'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'lgd': {
            'handlers': ['lgd'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}



# celery settings

CELERY_TASK_ROUTES = {
    'strategicbi.tasks.fetch_and_save_data': {'queue': 'data_tasks'},
}

CELERY_TIMEZONE = "Asia/Kolkata"
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_EXTENDED = True
CELERYD_CONCURRENCY = 4  
CELERYD_LOG_FORMAT = '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
CELERYD_LOG_FILE = 'celery.log'
CELERYBEAT_LOG_FILE = 'celerybeat.log'
CELERYD_POOL = 'gevent'  
CELERYD_PREFETCH_MULTIPLIER = 4  
CELERYD_MAX_TASKS_PER_CHILD = 100  
