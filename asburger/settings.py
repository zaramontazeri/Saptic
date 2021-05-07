"""
Django settings for partak project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
import datetime

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=3=wmc78&b=+$=-le=so2_i29$&+2u)e=@4anm8#=dxrnm$sbv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["46.4.203.185", 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'auth_rest_phone',
    'drf_yasg',
    'adminsortable2',  # link:https://django-admin-sortable2.readthedocs.io/en/latest/
    'rangefilter',  # link:https://github.com/silentsokolov/django-admin-rangefilter
    # link: https://django-rest-multiple-models.readthedocs.io/en/latest/
    'drf_multiple_model',
    # link: https://github.com/philipn/django-rest-framework-filters
    'rest_framework_filters',
    'users',
    'ckeditor',
    'ckeditor_uploader',  # link:https://django-ckeditor.readthedocs.io/en/latest/
    'embed_video',  # link:https://django-embed-video.readthedocs.io/en/latest/installation.html
    # 'django.contrib.sites',
    'nested_inline',

    'blog',
    'pages',
    'catalog',
    'shop',
    'corsheaders',
    'domains'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'asburger.urls'

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

WSGI_APPLICATION = 'asburger.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation

# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTHENTICATION_BACKENDS = [
    # 'users.auth.EmailMobileBackend',
    # 'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ]
}

AUTH_USER_MODEL = 'auth_rest_phone.UserProfile'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static/'

MEDIA_URL = '/uploads/'
MEDIA_ROOT = 'uploads/'

CKEDITOR_UPLOAD_PATH = 'uploads/ckeditor/'

TEMPLATE_DIRS = (os.path.join(BASE_DIR,  'templates'),)

# SWAGGER_SETTINGS = { #link:https://drf-yasg.readthedocs.io/en/stable/rendering.html
#    'DEFAULT_INFO': 'import.path.to.urls.api_info',
# }

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.serializers.RegisterSerializer',
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3600),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_PAYLOAD_HANDLER':
        'auth_rest_phone.custom_jwt_payload.jwt_payload_handler',
}


SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=60),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'JWT_PAYLOAD_HANDLER':
        'auth_rest_phone.custom_jwt_payload.jwt_payload_handler',
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,

    # 'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': datetime.timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': datetime.timedelta(days=1),
}


AUTH_REST = {
    'DOMAIN': 'asburger.ir',
    'SITE_NAME': 'asburger',
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_ACTIVATE_URL': 'password/reset/confirm_activate/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',
    # 'LOGIN_FIELD':"email",
    'ACTIVATION_URL': 'activate/{uid}/{token}',

    # 'ACTIVATION_RESET_URL': '#/reset_password_activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    "USER_CREATE_PASSWORD_RETYPE": True,
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": [
        "https://dafaritours.com",
        "http://localhost:3000"
        "https://localhost:8001/api/v1/auth/test_data",
        "https://dafaritours.com/api/v1/auth/test_data",
    ],
    'EMAIL': {
        'activation': 'auth_rest.email.ActivationEmail',
        'confirmation': 'auth_rest.email.ConfirmationEmail',
        'password_reset': 'auth_rest.email.PasswordResetEmail',
        'password_changed_confirmation': 'auth_rest.email.PasswordChangedConfirmationEmail',
        'username_changed_confirmation': 'auth_rest.email.UsernameChangedConfirmationEmail',
        'username_reset': 'auth_rest.email.UsernameResetEmail',
    },
    'SERIALIZERS': {
        'activation': 'auth_rest.serializers.ActivationSerializer',
        'password_reset': 'auth_rest.serializers.SendEmailResetSerializer',
        'password_reset_confirm': 'auth_rest.serializers.PasswordResetConfirmSerializer',
        'password_reset_confirm_retype': 'auth_rest.serializers.PasswordResetConfirmRetypeSerializer',
        'set_password': 'auth_rest.serializers.SetPasswordSerializer',
        'set_password_retype': 'auth_rest.serializers.SetPasswordRetypeSerializer',
        'set_username': 'auth_rest.serializers.SetUsernameSerializer',
        'set_username_retype': 'auth_rest.serializers.SetUsernameRetypeSerializer',
        'username_reset': 'auth_rest.serializers.SendEmailResetSerializer',
        'username_reset_confirm': 'auth_rest.serializers.UsernameResetConfirmSerializer',
        'username_reset_confirm_retype': 'auth_rest.serializers.UsernameResetConfirmRetypeSerializer',
        'user_create': 'users.serializers.UserPhoneNumberCreateSerializer',
        'user_create_password_retype': 'users.serializers.UserPhoneNumberCreatePasswordRetypeSerializer',
        'user_delete': 'auth_rest.serializers.UserDeleteSerializer',
        'user': 'auth_rest.serializers.UserSerializer',
        'current_user': 'auth_rest.serializers.UserSerializer',
        'token': 'auth_rest.serializers.TokenSerializer',
        'token_create': 'auth_rest.serializers.TokenCreateSerializer',
    },
}
CORS_ALLOW_ALL_ORIGINS =True
AUTH_SEND_SMS=True

ZARINPAL_MERCHANT = ""