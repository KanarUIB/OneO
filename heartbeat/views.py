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
Prüft ob ein erfolgreicher Heartbeat für jedes Software-Paket vorhanden ist, wenn das letzte
erfolgreiche Heartbeat vor über 24 Stunden einkam wird ein ausstehendes Heartbeat-Eintrag in der
Datenbank erstellt. 

Ist kein Heartbeat für ein Software-Paket vorhanden so wird ein Eintrag 
mit der Meldung "Heartbeat noch nie eingetroffen" erstellt.

"""""""""


def checkHeartbeat():
    softwarePakete = KundeHatSoftware.objects.all()
    for paket in softwarePakete:
        letzterHeartbeat = getLetzteHeartbeat(paket)

        if letzterHeartbeat is None:
            try:
                lizenz = Lizenz.objects.get(KundeHatSoftware=paket)

            except:

                lizenz = None

            if lizenz is not None:
                heartbeat = Heartbeat.objects.create(kundeSoftware=paket,
                                                     lizenzschluessel=lizenz.license_key,
                                                     meldung="Heartbeat noch nie eingetroffen",
                                                     datum=datetime.datetime.now())
            else:
                heartbeat = Heartbeat.objects.create(kundeSoftware=paket,
                                                     lizenzschluessel="Lizenzschlüssel konnte nicht gefunden werden",
                                                     meldung="Heartbeat noch nie eingetroffen",
                                                     datum=datetime.datetime.now())
        elif letzterHeartbeat.lizenzschluessel == "Lizenzschlüssel konnte nicht gefunden werden":
            Heartbeat.objects.filter(kundeSoftware=letzterHeartbeat.kundeSoftware,
                                     lizenzschluessel=letzterHeartbeat.lizenzschluessel).update(
                lizenzschluessel=Lizenz.objects.get(KundeHatSoftware=paket).license_key)
        else:
            timedelta = datetime.timedelta(hours=24)
            zeit = current_date - timezone.make_naive(letzterHeartbeat.datum)
            if zeit > timedelta:
                createMissingHeartbeats(letzterHeartbeat.kundeSoftware)


"""""""""
Erstellt einen Datenbank ausstehenden Heartbeat-Eintrag in der Tabelle Heartbeats für den angegebenen kundeHatSoftware Software-Paket
mit der Meldung "Heartbeat nicht eingetroffen".
@param kundeHatSoftware Software-Paket von einem spezifischen Standort/Kunden
"""""""""


def createMissingHeartbeats(kundeHatSoftware):
    heartbeat = Heartbeat.objects.create(kundeSoftware=kundeHatSoftware,
                                         lizenzschluessel=Lizenz.objects.get(
                                             KundeHatSoftware=kundeHatSoftware).license_key,
                                         meldung="Heartbeat nicht eingetroffen",
                                         datum=datetime.datetime.now())


"""""""""
Filtert aus allen Heartbeat-Objekten den aktuellsten Heartbeat-Objekte mit einer Error-Meldunge für den angegebenen softwarePaket heraus.
@param softwarePaket KundeHatSoftware-Objekt für welches die Error-Heartbeats gesucht werden sollen
"""""""""


def getErrorHeartbeats(softwarePaket):
    heartbeat = Heartbeat.objects.filter(kundeSoftware=softwarePaket).filter(meldung__icontains="Error").order_by(
        "datum").last()
    return heartbeat


"""""""""
Erstellt eine Liste von Heartbeats für die Ausgabe der ausstehenden und Fehlermeldung-Heartbeats auf der Dashboard-Seite
Hierfür betrachtet man den letzten erfolgreich eingangenen Heartbeat eines Software-Pakets und prüft, ob dessen Eingangsdatum
über 48 Stunden her ist. Heartbeats mit der Meldung "Noch nie eingetroffen" werden ebenso in die Liste hinzugefügt

@return negativeHeartbeats Alle negativen & error Heartbeats
"""""""""


def getNegativeHeartbeats():
    negativeHeartbeats = []
    softwarePakete = KundeHatSoftware.objects.all()
    for pakete in softwarePakete:

        # Hier werden der negativeHeartbeat-Liste alle Heartbeats die mit einer Error-Meldung hineinkamen
        # hinzugefügt.

        errorHeartbeats = getErrorHeartbeats(pakete)
        if errorHeartbeats is not None:
            negativeHeartbeats.append(errorHeartbeats)

        # Hier wird geprüft wann der letzter erfolgreiche Heartbeat für diesen jeweiligen Software-Paket
        # einkam, wenn dieser vor über 48 Stunden hineinkam wird der letzte Fehlende-Heartbeat in die Liste hinzugefügt

        heartbeat = Heartbeat.objects.filter(kundeSoftware=pakete).exclude(
            meldung="Heartbeat nicht eingetroffen").last()
        if heartbeat is None:
            negativeHeartbeats.append(getLetzteHeartbeat(pakete))
        else:
            timedelta = datetime.timedelta(hours=48)
            zeit = current_date - timezone.make_naive(heartbeat.datum)

            if zeit > timedelta:
                if getLetzteHeartbeat(pakete) not in negativeHeartbeats:
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

