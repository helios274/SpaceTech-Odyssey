from .production import *

STATIC_ROOT = BASE_DIR / 'static-files'

# Temporarily use the local filesystem for compression
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
COMPRESS_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Local path for compression to read/write files
COMPRESS_ROOT = STATIC_ROOT
