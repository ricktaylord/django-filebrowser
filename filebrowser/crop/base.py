from filebrowser.base import FileObject
from filebrowser.sites import get_breadcrumbs
from filebrowser.crop.settings import CROP_PREFIX, UNCROPPED_SOURCE_PREFIX
from filebrowser.settings import *

import os, tempfile
from django.core.files import File
# PIL import
if STRICT_PIL:
    from PIL import Image
else:
    try:
        from PIL import Image
    except ImportError:
        import Image

class CropDimensions(object):
    def __init__(self,x,y,w,h):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
    def __str__(self):
        return str(self.x)+"x"+str(self.y)+"x"+str(self.w)+"x"+str(self.h)
    @property
    def tuple(self):
        return (self.x,self.y,self.w,self,h)

class CropImageObject(FileObject):
    @property
    def is_crop_original(self):
        "True if file is source version, false otherwise"
        if self.is_version:
            return False
        tmp = self.filename_root.split("_")
        lent = len(tmp)
        if (lent>1 and tmp[lent - 1] != CROP_PREFIX) or tmp[lent - 1] == UNCROPPED_SOURCE_PREFIX:
            return True
        return False

    @property
    def crop_original(self):
        if self.is_crop_original:
            return self
        orig = self.original
        return FileObject(os.path.join(self.site.directory, self.head, self.crop_original_filename), site=self.site)

    @property
    def crop_original_filename(self):
        "Get the filename of an original image from a version"
        tmp = self.filename_root.split("_")
        if tmp[len(tmp) - 2] == CROP_PREFIX:
            return u"%s%s" % (re.sub(self.filename_root,"_"+CROP_PREFIX+"_.*",""), self.extension)
        return self.filename

    def crop_path(self, dimensions, name=None):
        return os.path.join(self.site.directory, self.head, self.crop_filename(dimensions,name))

    def crop_rel_path(self, dimensions, name=None):
        return os.path.join(self.head, self.crop_filename(dimensions,name))

    def crop_filename(self, dimensions, name=None):
        if not name:
            fname = str(dimensions)
        if name:
            fname+="x"+name
        return u"%s_%s_%s%s" % (self.filename_root, CROP_PREFIX, fname, self.extension)

    def crop_generate(self, x, y, w, h, name=None):
        dim = CropDimensions(x,y,w,h)
        source = self.crop_original
        crop_path = source.crop_rel_path(dim, name)
        crop_dir, crop_basename = os.path.split(crop_path)
        root, ext = os.path.splitext(crop_basename)
        tmpfile = File(tempfile.NamedTemporaryFile())
        try:
            f = source.site.storage.open(source.path)
        except IOError:
            return ""
        im = Image.open(f)
        crop = im.crop((x,y,x+w,y+h))
        if not crop:
            crop = im
        try:
            crop.save(tmpfile, format=Image.EXTENSION[ext.lower()], quality=VERSION_QUALITY, optimize=(os.path.splitext(crop_path)[1] != '.gif'))
        except IOError:
            crop.save(tmpfile, format=Image.EXTENSION[ext.lower()], quality=VERSION_QUALITY)
        if crop_path != self.site.storage.get_available_name(crop_path):
            self.site.storage.delete(crop_path)
        self.site.storage.save(crop_path, tmpfile)