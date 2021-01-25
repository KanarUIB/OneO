from django import forms
from .models import Kunde, Standort, KundeHatSoftware, Lizenz, Modul, Standortlizenz


class KundeCreateForms(forms.ModelForm):
    class Meta:
        model = Kunde
        fields = '__all__'


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


class SoftwareCreateForm(forms.ModelForm):
    class Meta:
        model = KundeHatSoftware
        fields = '__all__'


class ModulCreateForm(forms.ModelForm):
    class Meta:
        model = Modul
        fields = '__all__'


class StandortlizenzCreateForm(forms.ModelForm):
    class Meta:
        model = Standortlizenz
        fields = '__all__'


class StandortlizenzUpdateForm(forms.ModelForm):
    class Meta:
        model = Standortlizenz
        fields = '__all__'
