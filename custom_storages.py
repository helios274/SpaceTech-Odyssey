from storages.backends.gcloud import GoogleCloudStorage
from django.conf import settings


class StaticStorage(GoogleCloudStorage):
    location = 'static'
    bucket_name = settings.GS_BUCKET_NAME
