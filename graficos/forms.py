from django import forms
from .models import csvprint

class csvform(forms.ModelForm):
    class Meta:
        model = csvprint
        fields = ('cooperativa', 'ano', 'mes', 'csvfileref' )