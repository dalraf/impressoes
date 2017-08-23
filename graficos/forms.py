from django import forms
from .models import csv

class csvform(forms.ModelForm):
    class Meta:
        model = csv
        fields = ('cooperativa', 'ano', 'mes', 'csvfileref' )