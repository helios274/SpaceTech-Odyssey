import sentry_sdk
import logging
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
import os
from google.oauth2 import service_account
from .base import *

# Indicate production environment
os.environ.setdefault('DJANGO_ENV', 'production')

# Core overrides
DEBUG = False
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Sentry configuration
sentry_sdk.init(
    dsn=env('SENTRY_DSN'),
    integrations=[DjangoIntegration(), LoggingIntegration(
        level=logging.INFO,        # Capture info and above as breadcrumbs
        event_level=logging.ERROR  # Send errors as events
    )],
    traces_sample_rate=0.5,  # Adjust this for performance monitoring
    send_default_pii=True,   # To capture logged-in user info (PII)
    environment='production',
    debug=DEBUG,  # Enables SDK-level debugging in development
)

# Security hardening
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 60  # 60 days
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Google Cloud Storage for static (and media) files
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    BASE_DIR / 'sto-admin-sa.json'
)
GS_PROJECT_ID = env('GS_PROJECT_ID')
GS_BUCKET_NAME = env('GS_BUCKET_NAME')

STATIC_ROOT = BASE_DIR / 'static-files'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/static/'

# Compressor settings for production
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_ENABLED = False
COMPRESS_OFFLINE = True
COMPRESS_STORAGE = STATICFILES_STORAGE
COMPRESS_URL = STATIC_URL
