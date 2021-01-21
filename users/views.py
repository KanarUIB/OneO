from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm


"""""""""
Wird aufgerufen wenn der Nutzer sich auf dem Management Portal registrieren möchte.
Übergeben wird ein POST-Request mittels der Forms und in der Methode auf Richtigkeit geprüft.
Bei erfolgreicher Prüfung wird der Benutzer in der Datenbank anlegt und auf die Loginseite weitergeleitet und kann sich erfolgreich einloggen.
Bei fehlgeschlagener Prüfung wird der Benutzer aufgefordert die fehlerhaften Eingaben zu korrigieren/ergänzen.

@return render 
"""""""""


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Dein Account wurde kreiert! Du kannst dich nun anmelden {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
