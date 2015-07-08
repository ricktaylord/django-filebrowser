# coding: utf-8

# PYTHON IMPORTS
import os
import re

# DJANGO IMPORTS
from django import forms
from django.utils.translation import ugettext_lazy as _

# FILEBROWSER IMPORTS
from filebrowser.settings import FOLDER_REGEX
from filebrowser.utils import convert_filename
from filebrowser.base import OembedInfo

ALNUM_NAME_RE = re.compile(FOLDER_REGEX, re.U)

# CHOICES
TRANSPOSE_CHOICES = (
    ("", u"-----"),
    ("0", _(u"Flip horizontal")),
    ("1", _(u"Flip vertical")),
    ("2", _(u"Rotate 90° CW")),
    ("4", _(u"Rotate 90° CCW")),
    ("3", _(u"Rotate 180°")),
)


class CreateDirForm(forms.Form):
    """
    Form for creating a folder.
    """

    name = forms.CharField(widget=forms.TextInput(attrs=dict({'class': 'vTextField'}, max_length=50, min_length=3)), label=_(u'Name'), help_text=_(u'Only letters, numbers, underscores, spaces and hyphens are allowed.'), required=True)

    def __init__(self, path, *args, **kwargs):
        self.path = path
        self.site = kwargs.pop("filebrowser_site", None)
        super(CreateDirForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        "validate name"
        if self.cleaned_data['name']:
            # only letters, numbers, underscores, spaces and hyphens are allowed.
            if not ALNUM_NAME_RE.search(self.cleaned_data['name']):
                raise forms.ValidationError(_(u'Only letters, numbers, underscores, spaces and hyphens are allowed.'))
            # Folder must not already exist.
            if self.site.storage.isdir(os.path.join(self.path, convert_filename(self.cleaned_data['name']))):
                raise forms.ValidationError(_(u'The Folder already exists.'))
        return convert_filename(self.cleaned_data['name'])


class ChangeForm(forms.Form):
    """
    Form for renaming a file/folder.
    """

    custom_action = forms.ChoiceField(label=_(u'Actions'), required=False)
    name = forms.CharField(widget=forms.TextInput(attrs=dict({'class': 'vTextField'}, max_length=50, min_length=3)), label=_(u'Name'), help_text=_(u'Only letters, numbers, underscores, spaces and hyphens are allowed.'), required=True)

    def __init__(self, *args, **kwargs):
        self.path = kwargs.pop("path", None)
        self.fileobject = kwargs.pop("fileobject", None)
        self.site = kwargs.pop("filebrowser_site", None)
        super(ChangeForm, self).__init__(*args, **kwargs)

        # Initialize choices of custom action
        choices = [("", u"-----")]
        for name, action in self.site.applicable_actions(self.fileobject):
            choices.append((name, action.short_description))
        self.fields['custom_action'].choices = choices

    def clean_name(self):
        "validate name"
        if self.cleaned_data['name']:
            # only letters, numbers, underscores, spaces and hyphens are allowed.
            if not ALNUM_NAME_RE.search(self.cleaned_data['name']):
                raise forms.ValidationError(_(u'Only letters, numbers, underscores, spaces and hyphens are allowed.'))
            #  folder/file must not already exist.
            if self.site.storage.isdir(os.path.join(self.path, convert_filename(self.cleaned_data['name']))) and os.path.join(self.path, convert_filename(self.cleaned_data['name'])) != self.fileobject.path:
                raise forms.ValidationError(_(u'The Folder already exists.'))
            elif self.site.storage.isfile(os.path.join(self.path, convert_filename(self.cleaned_data['name']))) and os.path.join(self.path, convert_filename(self.cleaned_data['name'])) != self.fileobject.path:
                raise forms.ValidationError(_(u'The File already exists.'))
        return convert_filename(self.cleaned_data['name'])

class OembedUploadForm(forms.Form):
    """
    Form for getting files from Oembed services
    """
    urls = forms.CharField(widget=forms.TextInput(), label=_(u'URL(s) of file(s)'), help_text=_(u'Paste a URL (web address) or multiple URLs for files, from service that support OEmbed (e.g. Flickr)'), required=True)
    name = forms.CharField(widget=forms.TextInput(attrs=dict({'class': 'vTextField'}, max_length=50, min_length=3)), label=_(u'Name'), help_text=_(u'Only letters, numbers, underscores, spaces and hyphens are allowed.'), required=False)


    def clean_urls(self):
        "validate urls"
        if self.cleaned_data['urls']:
            urls = OembedInfo(self.cleaned_data['urls']).download_urls
            if not len(urls):
                raise forms.ValidationError(_(u'No downloadable URLs were recognised.  Make sure the service you are using supports oembed and has been added to the ProviderRules on this site.'))
            return urls
    def clean_name(self):
        "validate name"
        if self.cleaned_data['name']:
            # only letters, numbers, underscores, spaces and hyphens are allowed.
            if not ALNUM_NAME_RE.search(self.cleaned_data['name']):
                raise forms.ValidationError(_(u'Only letters, numbers, underscores, spaces and hyphens are allowed.'))
        return convert_filename(self.cleaned_data['name'])

