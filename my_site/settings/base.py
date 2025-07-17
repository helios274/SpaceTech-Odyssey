import os
from pathlib import Path
import environ
from django.contrib import messages
import cloudinary

# Base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Environment variable helper
env = environ.Env(
    DEBUG=(bool, False),
    CLOUDINARY_SECURE=(bool, True),
)

# Load environment variables from .env-prod file
env.read_env(BASE_DIR / '.env-prod')

# Core settings
SECRET_KEY = env('SECRET_KEY')

# Application definition
INSTALLED_APPS = [
    # Third‑party
    'django_browser_reload',
    'debug_toolbar',
    'compressor',

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local
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
WSGI_APPLICATION = 'my_site.wsgi.application'

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

# Database
DATABASES = {
    'default': env.db_url('DB_URI')
}

# Caches
CACHES = {
    'default': env.cache_url('REDIS_SERVER_URI', backend='django_redis.cache.RedisCache')
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

# Message tags
MESSAGE_TAGS = {messages.ERROR: 'danger'}

# Custom user & auth
AUTHENTICATION_BACKENDS = ['account.backends.EmailBackend']
AUTH_USER_MODEL = 'account.User'
LOGIN_URL = '/auth/login'

# Cloudinary configuration
cloudinary.config(
    cloud_name=env('CLOUDINARY_CLOUD_NAME'),
    api_key=env('CLOUDINARY_API_KEY'),
    api_secret=env('CLOUDINARY_API_SECRET'),
    secure=env('CLOUDINARY_SECURE'),
)
CLOUDINARY_ROOT_FOLDER = env('CLOUDINARY_ROOT_FOLDER')

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
