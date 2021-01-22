from django.shortcuts import render, redirect
import heartbeat.views as heartbeat_views
from heartbeat.models import Heartbeat
from .forms import StandortCreateForms, KundeCreateForms
from .models import Kunde, KundeHatSoftware, Software, Standort, Lizenz, Ansprechpartner
from django.http import JsonResponse, HttpResponse
import json
import datetime
from django.core.exceptions import ObjectDoesNotExist


"""""""""
Sammelt die Nutzerzahlen für alle vorhandenen Softwares in einer Liste
@return List Liste aller Software-Nutzerzahlen 
"""""""""

def getAmountUser():
    softwareUsers = []
    for software in Software.objects.all():
        softwareUsers.append(len(KundeHatSoftware.objects.filter(software=software)))
    return softwareUsers


"""""""""
Gibt eine Liste mit der Menge an Lizenzen die in den nächsten 30 Tagen, +30 Tagen oder 90 Tagen ablaufen werden.
Die Zahlen werden wie in der oben genannten Reihenfolge in die Liste hiznugefügt und wiedergeben.

@return List Menge der bald ablaufenden Lizenzen
"""""""""
def getLicenseDeltaDays():
    lizenzen = Lizenz.objects.all()
    licenseDeltaDays = []
    oneMonth = 0
    threeMonth=0
    others = 0
    for lizenz in lizenzen:
        tage_uebrig = lizenz.gültig_bis - datetime.date.today()
        if tage_uebrig.days <= 30:
            oneMonth += 1
        elif tage_uebrig.days <= 90:
            threeMonth += 1
        else:
            others += 1
    licenseDeltaDays.append(oneMonth)
    licenseDeltaDays.append(threeMonth)
    licenseDeltaDays.append(others)
    return licenseDeltaDays

"""""""""
Antwortet auf den Aufruf der Index-Seite mit den im context genannten Informationen und triggert 
die chechHeartbeat()-Methode, welches prüft, ob es ausstehende Heartbeats gibt.
@return render Gibt Dashboardseite mit den jeweiligen context Informationen aus.
"""""""""


def home(request):
    heartbeat_views.checkHeartbeat()
    context = {
        "kunde": Kunde.objects.all(),
        "softwares": Software.objects.all(),
        "khs": KundeHatSoftware.objects.all(),
        "heartbeats": heartbeat_views.getNegativeHeartbeats(),
        "lizenzenDelta": getLicenseDeltaDays(),
        "anzahlKunden": getAmountUser(),
    }
    return render(request, "dashboard.html", context)

"""""""""
Wird bei Aufruf der Kundenprofilseite aufgerufen.

Entnimmt aus dem Request die in der Domain übergebene Kunden ID und sucht in der Datenbank nach dem Kunden und all 
seinen Standorten.
Wenn die ID ungültig sein oder kein Kunden-Objekt für diese ID hinterlegt sein wird eine 404-Seite zurück gegeben.
Bei Erfolg wird durch den context alle Informationen zum Kunden, seinen Standorten, seiner genutzten Softwares und 
die dazugehörigen Heartbeats weitergegeben.

@return render Gibt die Kundenprofilseite ausgefüllt mit den jeweiligen Kundeninformationen aus.
"""""""""

def kundenprofil(request, id):
    print("bin drin")
    try:
        kunde = Kunde.objects.get(id=str(id))
        kundenStandorte = Standort.objects.filter(kunde=kunde)
        print(kundenStandorte)
    except ObjectDoesNotExist:
        return render(request,"404.html")

    if id is None or not kunde:
        return HttpResponse("404.html")

    if id is not None:

        context = {
            "kunde": kunde,
            "standorte": kundenStandorte,
            "softwarePakete": getStandortSoftware(kundenStandorte),
            "standortBerater": Ansprechpartner.objects.all(),
            "softwareLizenzen": Lizenz.objects.all(),
            "heartbeatHistorie": heartbeatHistorie(getStandortSoftware(kundenStandorte))
        }

    return render(request, "kundenprofil.html", context)


"""""""""
Wird bei Aufruf der Kundenseite aufgerufen.
Gibt durch den context alle in der Datenbank aufgefundenen Kunden zurück.

@return render Die Kundenseite mit allen in der Datenbank aufgefunden Kunden
"""""""""


def kunden(request):
    context = {
        "kunde": Kunde.objects.all(),
    }
    return render(request, "kunden.html", context)

"""""""""
Wird bei Aufruf der Lizenzseite aufgerufen.
Gibt durch den context alle in der Datenbank aufgefundenen Linzenzen zurück.

@return render Die Lizenzseite mit allen in der Datenbank aufgefunden Lizenzen
"""""""""
def lizenzen(request):
    context = {
        'lizenzen': Lizenz.objects.all(),
    }
    return render(request, "lizenz.html", context)

"""""""""
Wird bei Aufruf der Updateseite aufgerufen.
Gibt durch den context alle in der Datenbank aufgefundenen Lizenzen und Softwares zurück.

@return render Die Updateseite mit allen in dem context angegebenen Informationen
"""""""""
def updates(request):
    context = {
        'lizenzen': Lizenz.objects.all(),
        'softwares': Software.objects.all()
    }
    return render(request, 'updates.html', context)


"""""""""
Gibt alle Software-Pakete die, der im Parameter übergebenen Standorte, gehören in einer Liste zurück.

@return List Liste aller Software-Pakete eller Standorte aus dem Parameter
@param standort Ein spezifischer Standort eines Kunden
"""""""""


def getStandortSoftware(standorte):
    softwareVonKunde = []

    for standort in standorte:
        for software in KundeHatSoftware.objects.filter(standort = standort):
            softwareVonKunde.append(software)

    return softwareVonKunde

"""""""""
Gibt alle Heartbeats der im Parameter übergebenen Software-Pakete zurück.

@param softwarePakete
@return List Liste aller Heartbeats der übergebenen Software-Pakete
"""""""""


def heartbeatHistorie(softwarePakete):
    heartbeat_historie = []

    for paket in softwarePakete:
        for heartbeat in Heartbeat.objects.filter(kundeSoftware=paket):
            heartbeat_historie.append(heartbeat)

    return heartbeat_historie


def create_kunde(request):
    form = KundeCreateForms(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('kunden')
    context = {
        'form': form
    }
    return render(request, 'kunde/create_kunde.html', context)

def create_standort(request):
    form = StandortCreateForms(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('kundenprofil')
    context = {
        'form': form
    }
    return render(request, 'kunde/create_standort.html', context)
