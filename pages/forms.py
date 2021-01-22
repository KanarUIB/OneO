from django import forms
from .models import Kunde, Standort

class KundeCreateForms(forms.ModelForm):
    class Meta:
        model = Kunde
        fields = [
            'name',
            'vf_nummer'
        ]

class StandortCreateForms(forms.ModelForm):
    class Meta:
        model = Standort
        fields = [
            'kunde',
            'name',
            'plz',
            'ort',
            'strasse',
            'hausnr',
            'email',
            'telNr',
        ]
