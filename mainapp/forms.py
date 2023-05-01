from django import forms


class UploadForm(forms.Form):
    authors = forms.FileField()
    papers = forms.FileField()
    affiliations = forms.FileField()
    conferences = forms.FileField()
