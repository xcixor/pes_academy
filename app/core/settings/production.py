from .base import *
DEBUG = True
CPANEL_HOSTING = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')
# STATICFILES_DIRS = [
# '/home/dianagic/applications/core',
# ]

STATIC_URL = '/static/'
STATIC_ROOT = '/home/dianagic/applications.privateequity-support.com/static'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#HTTPS SETTING
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# ckeditor config
CKEDITOR_BASEPATH = '/static/ckeditor/ckeditor/'
