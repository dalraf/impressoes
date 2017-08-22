from django import forms

from .models import CVSFiles

class CVSform(forms.ModelForm):
    class Meta:
        model = CVSFiles
        fields = ('cvs', )