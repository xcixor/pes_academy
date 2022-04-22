from .base import *
from google.oauth2 import service_account


DEBUG = False

# static files settings
STATIC_ROOT = os.environ.get('GS_BUCKET_URL') + 'static/'
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'


# media files config
MEDIA_URL = os.environ.get('GS_BUCKET_URL')
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')
GS_LOCATION = os.environ.get('GS_LOCATION')

GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.environ.get('GS_CREDENTIALS')
)
