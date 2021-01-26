from django import forms
from .models import Kunde, Standort, KundeHatSoftware, Lizenz, Modul, Standortlizenz


class KundeCreateForms(forms.ModelForm):
    """
        Das KundeCreateForms ist die Forms zur Erstellung eines Kunden.
        Es bildet das Model Kunde mit all seinen Attributen ab.

        Parameters:
            data: Das KundeCreateForm kann jegliche Daten aufnehmen, welche zu einem Kunden gehören.
    """

    class Meta:
        """
            model :     Das Model, welches die Forms abbildet.
            fields :    Die Attribute des Models die man in der Forms abfragen möchte -> '__all__' bildet alle Attributen des Modells ab
        """

        model = Kunde
        fields = '__all__'


class StandortCreateForms(forms.ModelForm):
    """
        Das StandortCreateForms ist die Forms zur Erstellung eines Standortes.
        Es bildet das Model Standort mit all seinen Attributen ab.

        Parameters:
            data: Das StandortCreateForm kann jegliche Daten aufnehmen, welche zu einem Standort gehören.
    """

    class Meta:
        """
            model :     Das Model, welches die Forms abbildet.
            fields :    Die Attribute des Models die man in der Forms abfragen möchte -> '__all__' bildet alle Attributen des Modells ab
        """

        model = Standort
        fields = '__all__'


class SoftwareCreateForm(forms.ModelForm):
    """
        Das SoftwareCreateForms ist die Forms zur Erstellung eines KundeHatSoftware.
        Es bildet das Model KundeHatSoftware mit all seinen Attributen ab.

        Parameters:
            data: Das SoftwareCreateForm kann jegliche Daten aufnehmen, welche zu einem KundeHatSoftware-Paket gehören.
    """

    class Meta:
        """
            model :     Das Model, welches die Forms abbildet.
            fields :    Die Attribute des Models die man in der Forms abfragen möchte -> '__all__' bildet alle Attributen des Modells ab
        """

        model = KundeHatSoftware
        fields = '__all__'


class StandortlizenzCreateForm(forms.ModelForm):
    """
        Das StandortlizenzCreateForms ist die Forms zur Erstellung eines Standortlizenzes.
        Es bildet das Model Standortlizenz mit all seinen Attributen ab.

        Parameters:
            data: Das StandortlizenzCreateForm kann jegliche Daten aufnehmen, welche zu einem Standortlizenzen gehören.
    """

    class Meta:
        """
            model :     Das Model, welches die Forms abbildet.
            fields :    Die Attribute des Models die man in der Forms abfragen möchte -> '__all__' bildet alle Attributen des Modells ab
        """
        model = Standortlizenz
        fields = '__all__'
