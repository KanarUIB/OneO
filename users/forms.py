from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    """
        Das UserRegisterForm ist die Forms zur Erstellung eines Users.
        Dies wird benötigt, um einen Benutzer in dem Management Portal anzulegen.
        Hierfür wird das von Django gelieferten User Bibliotheke genutzt.

        Parameters:
            data: Das UserRegisterForm kann jegliche Daten aufnehmen, welche zu einem User gehören.
    """

    email = forms.EmailField()

    class Meta:
        """
            model :     Das Model, welches die Forms abbildet.
            fields :    Die Attribute die benötigt werden, um einen User anzulegen.
        """

        model = User
        fields = ['username', 'email', 'password1', 'password2']
