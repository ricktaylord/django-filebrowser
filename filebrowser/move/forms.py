from django import forms
class MoveForm(forms.Form):
    """ 
    Form for moving files on server
    """
    path = forms.CharField(widget=forms.TextInput(), label="Move to folder: uploads/", required=False)