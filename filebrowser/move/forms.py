from django import forms
class MoveForm(forms.Form):
    """ 
    Form for 
    """
    path = forms.CharField(widget=forms.TextInput(), label="Server path (no leading slash)")