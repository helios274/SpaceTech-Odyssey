from .base import *

# Development-specific settings
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
INTERNAL_IPS = ['127.0.0.1']


# Static files (collected and served locally)
STATIC_ROOT = BASE_DIR / 'static-files'
STATICFILES_DIRS = [BASE_DIR / 'static']


# Django Compressor in development
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False
