from filebrowser.base import FileObject
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect
from filebrowser.sites import get_breadcrumbs
from filebrowser.templatetags.fb_tags import query_helper
from django.template import RequestContext as Context
from django.contrib import messages
from django.core.urlresolvers import reverse
from django import forms
import os


class MoveViews(object):
    def __init__(self, site):
        self.site = site
    def main(self, request):
        """
        Move file/folder 
        """
        from filebrowser.move.forms import MoveForm
        site = self.site
        query = request.GET
        path = os.path.join(site.directory, query.get('dir', ''))
        fileobject = FileObject(os.path.join(path, query.get('filename', '')), site=site) 
        msg = ""

        if request.method == "POST":
            form = MoveForm(request.POST)
            if form.is_valid():
                path = form.cleaned_data['path']
                destobject = FileObject(os.path.join(site.directory,path,fileobject.filename),site=site)
                try:
                    site.storage.move(fileobject.path,destobject.path)
                    # MESSAGE & REDIRECT
                    msg = _('The file %s was successfully moved to location %s.') % (fileobject.path, destobject.path)
                    messages.success(request,msg)
                    redirect_url = reverse("filebrowser:fb_browse") + query_helper(query, "", "filename,filetype")
                    return HttpResponseRedirect(redirect_url)
                except OSError as e:
                    form.errors['path'] = forms.util.ErrorList([_(e.message)])
        else:
            form = MoveForm()

        return render_to_response('filebrowser/move.html', {
            'title': _(u'Move "%s"') % fileobject.filename,
            'form': form,
            'query': query,
            'breadcrumbs': get_breadcrumbs(query, path),
            'breadcrumbs_title': _(u'Move file')
        }, context_instance=Context(request,current_app=site.name))
