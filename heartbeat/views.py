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
import json
from django.http import JsonResponse
from django.core import serializers

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
    """
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

    """


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


"""""""""
REST-API die zum Empfangen aller Heartbeat-Requests dient.

Das Heartbeat-Request muss aus dem Lizenzschlüssel und einem Statusbericht der Software bestehen.
Bei Eingang eines Requests werden anhand des empfangenen Lizenznschlüssels das Lizenz-Objekt aus der Datenbank gefiltert,
der dazugehörige Software-Paket ermittelt und der aktuelle Zeitpunkt notiert, um mit all diesen Daten den Heartbeat Eintrag
in der Datenbank erstellen zu können.

Als Response wird der Lizenzschlüssel zurück gegeben.
"""""""""


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



@api_view(["POST"])
def lizenzHeartbeat(request):
    beat = {
        "lizenzschluessel": request.data["lizenzschluessel"]
    }

    """""""""
    #Instanziere alle nötigen Attribute für einen Heartbeat
    """""""""
    license = Lizenz.objects.get(license_key=beat["lizenzschluessel"])

    kundeSoftware = license.KundeHatSoftware
    datum = datetime.date.today()
    #startdate = license.gültig_von
    enddate = license.gültig_bis

    if enddate < datum and license.replace_key:
        return JsonResponse(json.dumps({"lizenz" : license.replace_key.license_key, "exist": True}), safe=False)

    elif enddate > datum or license.replace_key == None:
        return JsonResponse(json.dumps({"lizenz": "", "exist": False}), safe=False)

    else:
        '''
        try:
            location_license = license.objects.get(key=beat["key"])
            print(location_license.key)
            used_software_product = KundeHatSoftware.objects.get(
                location = location_license.location,
                product  = location_license.module.product,
            )
            Heartbeat.objects.create(used_product=used_software_product, message=beat["key"], detail=beat["log"])
        except:
            try:
                customer_license = license.objects.get(key=beat["key"])
                print(customer_license.key)
                locations = Location.objects.filter(customer = customer_license.customer)
                for location in locations:
                    used_software_product = UsedSoftwareProduct.objects.get(
                        location = location,
                        product  = customer_license.module.product,
                    )
                    break
                Heartbeat.objects.create(used_product=used_software_product, message=beat["key"], detail=beat["log"], unknown_location = True)
            except:
                pass
        '''
    Heartbeat.objects.create(kundeSoftware=kundeSoftware, lizenzschluessel=beat["lizenzschluessel"],
                             meldung=beat["meldung"],
                             datum=datum)
    return Response(beat["lizenzschluessel"])



# API für das überschreiben der Lizenzen
@api_view(["POST"])
def lizenzSave(request):

    if request.data["bool"] == "True":

        replace = Lizenz.objects.get(license_key=request.data["new"])
        gueltig_von = replace.gültig_von
        gueltig_bis = replace.gültig_bis

        Lizenz.objects.get(license_key=request.data["new"], replace_key=None).delete()
        Lizenz.objects.filter(license_key=request.data["old"]).update(license_key=request.data["new"], gültig_von=gueltig_von, gültig_bis=gueltig_bis, replace_key=None)



    return JsonResponse({})

