# coding: utf-8

# PYTHON IMPORTS
import os
import re


# DJANGO IMPORTS
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

# FILEBROWSER IMPORTS
from filebrowser.settings import EXTENSION_LIST, EXCLUDE, DIRECTORY, VERSIONS, EXTENSIONS
from filebrowser.base import FileListing, FileObject
from filebrowser.sites import site


filter_re = []
for exp in EXCLUDE:
    filter_re.append(re.compile(exp))
for k, v in VERSIONS.items():
    exp = (r'_%s(%s)') % (k, '|'.join(EXTENSION_LIST))
    filter_re.append(re.compile(exp))


class Command(BaseCommand):
    args = '<media_path>'
    help = "Flag originals as such with the storage."

    def handle(self, *args, **options):
        media_path = ""

        if len(args):
            media_path = args[0]
            path = media_path
        else:
            path = DIRECTORY

        if not site.storage.isdir(os.path.join(settings.MEDIA_ROOT, path)):
            raise CommandError(
                '<media_path> must be a directory in MEDIA_ROOT (If you don\'t add a media_path the default path is DIRECTORY).\n"%s" is no directory.' % path)

        # filelisting
        # FIXME filterfunc: no hidden files, exclude list, no versions, just
        # images!
        paths = [k for k,v in site.storage.entries.iteritems() if self.filter_images(v)]
        
        site.storage.batch_set_original(paths)

    def filter_images(self, item):
        filename = item.path.split("/")[-1]
        filtered = filename.startswith('.')
        for re_prefix in filter_re:
            if re_prefix.search(filename):
                filtered = True
        if filtered:
            return False
        return True
