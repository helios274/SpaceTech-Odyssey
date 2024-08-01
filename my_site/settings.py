import os
from pathlib import Path
from django.contrib import messages
from environ import Env
from google.oauth2 import service_account
import dj_database_url
import cloudinary.uploader
import cloudinary

env = Env(
    DEBUG=(bool, False),
    CLOUDINARY_SECURE=(bool, True),
)

BASE_DIR = Path(__file__).resolve().parent.parent

Env.read_env(BASE_DIR / '.env')  # Get environment variables from .env file

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = list(
    env.list('ALLOWED_HOSTS', default=['127.0.0.1'])
)


INSTALLED_APPS = [
    'django_browser_reload',
    'debug_toolbar',
    'compressor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'account',
]

MIDDLEWARE = [
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'my_site.wsgi.app'

DATABASES = {
    'default': dj_database_url.parse(env('DB_URI'))
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


if DEBUG:
    INTERNAL_IPS = [
        "127.0.0.1",
    ]
    STATIC_ROOT = BASE_DIR / 'static'
    STATIC_URL = '/static/'

else:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    STATICFILES_DIRS = [
        BASE_DIR / 'static'
    ]

    # Google cloud storage settings
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        os.path.join(BASE_DIR, 'sto-admin-sa.json')
    )
    GS_PROJECT_ID = env('GS_PROJECT_ID')
    GS_BUCKET_NAME = env('GS_BUCKET_NAME')

    STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/static/'


COMPRESS_ROOT = BASE_DIR / 'static'  # django-compressor

COMPRESS_ENABLED = True  # django-compressor

# django-compressor
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]


MESSAGE_TAGS = {
    messages.ERROR: "danger"
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = ['account.backends.EmailBackend']

AUTH_USER_MODEL = 'account.User'

LOGIN_URL = '/auth/login'

cloudinary.config(
    cloud_name=env('CLOUDINARY_CLOUD_NAME'),
    api_key=env('CLOUDINARY_API_KEY'),
    api_secret=env('CLOUDINARY_API_SECRET'),
    secure=env('CLOUDINARY_SECURE')
)

CLOUDINARY_ROOT_FOLDER = env('CLOUDINARY_ROOT_FOLDER')
