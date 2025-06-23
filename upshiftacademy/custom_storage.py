from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    querystring_auth = False

class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
    default_acl = None
    querystring_auth = False

    