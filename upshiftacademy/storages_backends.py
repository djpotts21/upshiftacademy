"""Storage backends for static and media files using S3."""
from storages.backends.s3boto3 import S3Boto3Storage
import logging
logger = logging.getLogger(__name__)


class StaticStorage(S3Boto3Storage):
    """Storage class for static files on S3."""
    location = 'static'
    default_acl = 'public-read'
    
    def __init__(self, *args, **kwargs):
        logger.warning("✅ Using S3 StaticStorage backend")
        super().__init__(*args, **kwargs)


class MediaStorage(S3Boto3Storage):
    """Storage class for media files on S3."""
    location = 'media'
    file_overwrite = False
