# Create your views here.
#   untenstehenden TEST-Befehl auf Kundenseite integrieren in Verbindung mit cronjob im Format */10 * * * * ... (alle 10 Minuten)
#   curl -X POST -d kdNr=1;mandant=Mercedes_GmbH;software=aurep;lizenz=True localhost:8000/heartbeat
from django.shortcuts import redirect, render
import asyncio
import random
import pathlib
import ssl
import websockets

from .models import Heartbeat
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pages.models import Lizenz, KundeHatSoftware
import datetime
from django.utils import timezone
import schedule

current_date = datetime.datetime.now()


def getLetzteHeartbeat(kundeHatSoftware):
    return Heartbeat.objects.filter(kundeSoftware=kundeHatSoftware).order_by('datum').last()


"""""""""
Checks if there is a Heartbeat for the specific KundeHatSoftware kundeHatSoftware on that day.
Return True if there is a Heartbeat object or False if there is no Heartbeat object for kundeHatSoftware.
"""""""""


def checkHeartbeat():
    softwarePakete = KundeHatSoftware.objects.all()
    for paket in softwarePakete:
        letzterHeartbeat = getLetzteHeartbeat(paket)
        if letzterHeartbeat is None:
            heartbeat = Heartbeat.objects.create(kundeSoftware=paket,
                                                 lizenzschluessel=Lizenz.objects.get(
                                                     KundeHatSoftware=paket).license_key,
                                                 meldung="Heartbeat noch nie eingetroffen",
                                                 datum=datetime.datetime.now())
        else:
            timedelta = datetime.timedelta(hours=24)
            zeit = current_date - timezone.make_naive(letzterHeartbeat.datum)
            if zeit > timedelta:
                createMissingHeartbeats(letzterHeartbeat.kundeSoftware)


"""""""""
Creates Database Entries for the missing Heartbeats after checking if there is a heartbeat
for the specific KundeHatSoftware.
@param kundeHatSoftware Software-Paket von einem spezifischen Standort/Kunden
"""""""""


def createMissingHeartbeats(kundeHatSoftware):
    heartbeat = Heartbeat.objects.create(kundeSoftware=kundeHatSoftware,
                                         lizenzschluessel=Lizenz.objects.get(
                                             KundeHatSoftware=kundeHatSoftware).license_key,
                                         meldung="Heartbeat nicht eingetroffen",
                                         datum=datetime.datetime.now())


def getErrorHeartbeats(softwarePaket):
        heartbeat = Heartbeat.objects.filter(kundeSoftware=softwarePaket).filter(meldung__icontains="Error").order_by(
            "datum").last()
        return heartbeat


"""""""""

@return negativeHeartbeats Alle negativen Heartbeats
"""""""""
def getNegativeHeartbeats():
    negativeHeartbeats = []
    softwarePakete = KundeHatSoftware.objects.all()
    for pakete in softwarePakete:

        #Hier werden der negativeHeartbeat-Liste alle Heartbeats die mit einer Error-Meldung hineinkamen
        #hinzugefügt.

        errorHeartbeats = getErrorHeartbeats(pakete)
        if errorHeartbeats is not None:
            negativeHeartbeats.append(errorHeartbeats)

        #Hier wird geprüft wann der letzter erfolgreiche Heartbeat für diesen jeweiligen Software-Paket
        #einkam, wenn dieser vor über 48 Stunden hineinkam wird der letzte Fehlende-Heartbeat in die Liste hinzugefügt

        heartbeat = Heartbeat.objects.filter(kundeSoftware=pakete).exclude(
            meldung="Heartbeat nicht eingetroffen").last()
        if heartbeat is None:
            negativeHeartbeats.append(getLetzteHeartbeat(pakete))
        else:
            timedelta = datetime.timedelta(hours=48)
            zeit = current_date - timezone.make_naive(heartbeat.datum)
            print("heartbeat:" + str(heartbeat))
            print(zeit)
            print("timedelta " + str(timedelta))
            if zeit > timedelta:
                if getLetzteHeartbeat(pakete) not in negativeHeartbeats:
                    print("negative:" + str(negativeHeartbeats))
                    negativeHeartbeats.append(getLetzteHeartbeat(pakete))
            elif heartbeat.meldung == "Heartbeat noch nie eingetroffen":
                negativeHeartbeats.append(heartbeat)
    return negativeHeartbeats


@api_view(["POST"])
def heartbeat(request):
    beat = {
        "lizenzschluessel": request.data["lizenzschluessel"],
        "meldung": request.data["meldung"],
    }
    print(beat["lizenzschluessel"])
    print(beat["meldung"])
    """""""""
    #Instanziere alle nötigen Attribute für einen Heartbeat
    """""""""
    license = Lizenz.objects.get(license_key=beat["lizenzschluessel"])

    kundeSoftware = license.KundeHatSoftware
    datum = datetime.datetime.now()

    Heartbeat.objects.create(kundeSoftware=kundeSoftware, lizenzschluessel=beat["lizenzschluessel"],
                             meldung=beat["meldung"],
                             datum=datum)
    return Response(beat["lizenzschluessel"])


""""""
{
    "lizenzschluessel": "APSDASDQ123123ASDLKA1231",
    "meldung": "Error: Couldn't fetch data"
}

""""""
