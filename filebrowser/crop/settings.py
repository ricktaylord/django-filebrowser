
from django.conf import settings

# Crop edit screen version
CROP_EDIT_VERSION = getattr(settings, 'FILEBROWSER_CROP_EDIT_VERSION', 'big')
# Crop preview version
CROP_PREVIEW_VERSION = getattr(settings, 'FILEBROWSER_CROP_PREVIEW_VERSION', 'small')
# Uncropped image label
UNCROPPED_SOURCE_PREFIX = getattr(settings, 'FILEBROWSER_UNCROPPED_SOURCE_PREFIX', 'uncropped')
CROP_PREFIX = getattr(settings, 'FILEBROWSER_CROP_PREFIX', 'crop')