from django import forms
class CropForm(forms.Form):
    """ 
    Form for cropping an image file. Intended to work with jCrop.
    """
    x = forms.IntegerField(widget=forms.HiddenInput())
    y = forms.IntegerField(widget=forms.HiddenInput())
    w = forms.IntegerField(widget=forms.HiddenInput())
    h = forms.IntegerField(widget=forms.HiddenInput())