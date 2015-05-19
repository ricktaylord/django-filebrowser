from filebrowser.base import FileObject
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect
from filebrowser.sites import get_breadcrumbs
from filebrowser.templatetags.fb_tags import query_helper
from django.template import RequestContext as Context
from django.contrib import messages
from django.core.urlresolvers import reverse
from filebrowser.crop.settings import CROP_PREVIEW_VERSION, CROP_EDIT_VERSION
import os

class CropViews(object):
    def __init__(self, site):
        self.site = site
    def main(self, request):
        """
        Crop existing image.
        """
        from filebrowser.crop.base import CropImageObject
        from filebrowser.crop.forms import CropForm
        site = self.site
        query = request.GET
        path = u'%s' % os.path.join(site.directory, query.get('dir', ''))
        fileobject = CropImageObject(os.path.join(path, query.get('filename', '')), site=site)
        original = fileobject.crop_original
        cropped = None
        msg = ""

        if request.method == "POST":
            form = CropForm(request.POST)
            if form.is_valid():
                x = form.cleaned_data['x']
                y = form.cleaned_data['y']
                w = form.cleaned_data['w']
                h = form.cleaned_data['h']
                try:
                    cropped_path = original.crop_generate(x,y,w,h)
                    # MESSAGE & REDIRECT
                    msg = _('The image file %s was successfully cropped to file %s.') % (original.filename_lower, cropped_path)
                    messages.success(request,message=msg)
                    redirect_url = reverse("filebrowser:fb_browse") + query_helper(query, "", "filename,filetype")
                    return HttpResponseRedirect(redirect_url)
                except OSError, (errno, strerror):
                    form.errors['name'] = forms.util.ErrorList([_('Error.')])
        else:
            form = CropForm()

        return render_to_response('filebrowser/crop.html', {
            'title': _(u'Crop "%s"') % original.filename,
            'form': form,
            'query': query,
            'cropped': cropped,
            'uncropped': original,
            'uncropped_url': original.url,
            'preview_version': CROP_PREVIEW_VERSION,
            'edit_version': CROP_EDIT_VERSION,
            'breadcrumbs': get_breadcrumbs(query, path),
            'breadcrumbs_title': _(u'Crop')
        }, context_instance=Context(request,current_app=site.name))
