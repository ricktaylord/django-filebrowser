from filebrowser.base import FileObject

from filebrowser.sites import FileBrowserSite

def crop_main(self, request):
    """
    Crop existing image.
    """
    query = request.GET
    path = u'%s' % os.path.join(self.directory, query.get('dir', ''))
    fileobject = FileObject(os.path.join(path, query.get('filename', '')), site=self)
    original = fileobject.crop_original
    cropped = FileObject()
    
    msg = ""

    if request.method == "POST":
        
        form = CropForm(abs_path, file_extension, request.POST)
        if form.is_valid():
            x = form.cleaned_data['x']
            y = form.cleaned_data['y']
            w = form.cleaned_data['w']
            h = form.cleaned_data['h']
            try:
                # PRE DELETE SIGNAL
                filebrowser_pre_crop.send(sender=request, orig_obj=original, cropped_obj=cropped, x=x, y=y, w=w, h=h)
                crop_image(fileobject, x, y, w, h)
                filebrowser_post_crop.send(sender=request, orig_obj=original, cropped_obj=cropped, x=x, y=y, w=w, h=h)
                # MESSAGE & REDIRECT
                msg = _('The image file %s was successfully cropped.') % (original.filename_lower)
                messages.success(request,message=msg)
                redirect_url = reverse("fb_browse") + query_helper(query, "", "filename,filetype")
                return HttpResponseRedirect(redirect_url)
            except OSError, (errno, strerror):
                form.errors['name'] = forms.util.ErrorList([_('Error.')])
    else:
        form = CropForm(abs_path, file_extension)

                
                
    return render_to_response('filebrowser/crop.html', {
        'title': _(u'Crop "%s"') % filename,
        'form': form,
        'query': query,
        'dir': query.get('dir', ''),
        'cropped': cropped.relative_url,
        'uncropped_width': uncropped.width,
        'uncropped_height': uncropped.height,
        'uncropped': uncropped.relative_url,
        'preview_version': CROP_PREVIEW_VERSION,
        'edit_version': CROP_EDIT_VERSION,
        'breadcrumbs': get_breadcrumbs(query, path),
        'breadcrumbs_title': _(u'Crop')
    }, context_instance=Context(request))

storage = DefaultStorage()
# Default FileBrowser site
site = CropFileBrowserSite(name='filebrowser', storage=storage)

# Default actions
from filebrowser.actions import flip_horizontal, flip_vertical, rotate_90_clockwise, rotate_90_counterclockwise, rotate_180
site.add_action(flip_horizontal)
site.add_action(flip_vertical)
site.add_action(rotate_90_clockwise)
site.add_action(rotate_90_counterclockwise)
site.add_action(rotate_180)