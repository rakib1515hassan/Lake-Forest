import os
from pathlib import Path
from datetime import timedelta
from decouple import config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-_bt&#bbqabhv+4$v4mg32$+0qz*o&j7kg5fl)uzz&*0jg_06!9'
SECRET_KEY = config('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)



ALLOWED_HOSTS = []


## For Custom User Model
AUTH_USER_MODEL ='users.User'
swappable = 'AUTH_USER_MODEL'


# My Apps
CUSTOM_APPS = [
    'apps.core.apps.CoreConfig',
    'apps.dashboards.apps.DashboardsConfig',
    'apps.users.apps.UsersConfig',
    'apps.events.apps.EventsConfig',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    # 'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',

] + CUSTOM_APPS



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lake_forest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates') ],
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

WSGI_APPLICATION = 'lake_forest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE"  : "django.db.backends.postgresql",
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        "NAME"    : config('DB_NAME'),      
        "USER"    : config('DB_USER'),           
        "PASSWORD": config('DB_PASSWORD'),           
        "HOST"    : config('DB_HOST'),
        "PORT"    : config('DB_PORT'),

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "/static")
STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'static/')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



DEFAULT_PAGINATION_LIMIT = 2

# FORM_RENDERER = 'address_backend.forms.CustomDivFormRenderer'


# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST    = config('EMAIL_HOST', default='localhost')
EMAIL_PORT    = config('EMAIL_PORT', default=25, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)

EMAIL_HOST_USER     = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')


OTP_TIMEOUT = 30  ## OTP timeout set 3 minutes


REST_FRAMEWORK = {
    
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],

    'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),

    # 'DEFAULT_FILTER_BACKENDS': [
    #         'django_filters.rest_framework.DjangoFilterBackend'
    #     ],
    
}

# JWT Token time set
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME":  timedelta(days=3),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=20),
}