from storages.backends.gcloud import GoogleCloudStorage
from django.conf import settings


class StaticStorage(GoogleCloudStorage):
    location = 'static-files'
    bucket_name = settings.GS_BUCKET_NAME
