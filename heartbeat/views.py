from .models import Heartbeat
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pages.models import Lizenz, KundeHatSoftware
import datetime
from django.utils import timezone
import json
from django.http import JsonResponse

current_date = datetime.datetime.now()


def getLetzteHeartbeat(kundeHatSoftware):
    return Heartbeat.objects.filter(kundeSoftware=kundeHatSoftware).order_by('datum').last()





def checkHeartbeat():
    """
    Prüft ob ein erfolgreicher Heartbeat für jedes Software-Paket vorhanden ist, wenn das letzte
    erfolgreiche Heartbeat vor über 24 Stunden einkam wird ein ausstehendes Heartbeat-Eintrag in der
    Datenbank erstellt.

    Ist kein Heartbeat für ein Software-Paket vorhanden so wird ein Eintrag
    mit der Meldung "Heartbeat noch nie eingetroffen" erstellt.
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
                Heartbeat.objects.create(kundeSoftware=paket,
                                                     lizenzschluessel=lizenz.license_key,
                                                     meldung="Heartbeat noch nie eingetroffen",
                                                     datum=datetime.datetime.now())
            else:
                Heartbeat.objects.create(kundeSoftware=paket,
                                                     lizenzschluessel="Lizenzschlüssel konnte nicht gefunden werden",
                                                     meldung="Heartbeat noch nie eingetroffen",
                                                     datum=datetime.datetime.now())
        else:
            timedelta = datetime.timedelta(hours=24)
            zeit = current_date - timezone.make_naive(letzterHeartbeat.datum)
            if zeit > timedelta:
                createMissingHeartbeats(letzterHeartbeat.kundeSoftware)





def createMissingHeartbeats(kundeHatSoftware):
    """
    Erstellt einen Datenbank ausstehenden Heartbeat-Eintrag in der Tabelle Heartbeats für den angegebenen kundeHatSoftware Software-Paket
    mit der Meldung "Heartbeat nicht eingetroffen".

    Parameters:
        kundeHatSoftware:                    Software-Paket von einem spezifischen Standort/Kunden
    """
    heartbeat = Heartbeat.objects.create(kundeSoftware=kundeHatSoftware,
                                         lizenzschluessel=Lizenz.objects.get(
                                             KundeHatSoftware=kundeHatSoftware).license_key,
                                         meldung="Heartbeat nicht eingetroffen",
                                         datum=datetime.datetime.now())





def getErrorHeartbeats(softwarePaket):
    """"
    Filtert aus allen Heartbeat-Objekten den aktuellsten Heartbeat-Objekte mit einer Error-Meldunge für den angegebenen softwarePaket heraus.

    Parameters:
        softwarePaket (QuerySet):           KundeHatSoftware-Objekt für welches die Error-Heartbeats gesucht werden sollen

    Return:
        heartbeat (Queryset):
    """
    heartbeat = Heartbeat.objects.filter(kundeSoftware=softwarePaket).filter(meldung__icontains="Error").order_by(
        "datum").last()
    return heartbeat





def getNegativeHeartbeats():
    """
    Erstellt eine Liste von Heartbeats für die Ausgabe der ausstehenden und Fehlermeldung-Heartbeats auf der Dashboard-Seite
    Hierfür betrachtet man den letzten erfolgreich eingangenen Heartbeat eines Software-Pakets und prüft, ob dessen Eingangsdatum
    über 48 Stunden her ist. Heartbeats mit der Meldung "Noch nie eingetroffen" werden ebenso in die Liste hinzugefügt

    Returns:
        negativeHeartbeats (list):                 Alle negativen & error Heartbeats
    """
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
    """
    REST-API die zum Empfangen aller Heartbeat-Requests dient.

    Das Heartbeat-Request muss aus dem Lizenzschlüssel und einem Statusbericht der Software bestehen.
    Bei Eingang eines Requests werden anhand des empfangenen Lizenznschlüssels das Lizenz-Objekt aus der Datenbank gefiltert,
    der dazugehörige Software-Paket ermittelt und der aktuelle Zeitpunkt notiert, um mit all diesen Daten den Heartbeat Eintrag
    in der Datenbank erstellen zu können.

    Als Response wird der Lizenzschlüssel zurück gegeben.

    Parameters:
        request (JSON):                Der HTTP Request des Clients in welchem sich der lizenzschluessel und die meldung befinden

    Returns:
        Response (dict):                Der Lizenzschlüssel wird im Response zurückgesendet (keine weiteren Auswirkungen)
    """
    beat = {
        "lizenzschluessel": request.data["lizenzschluessel"],
        "meldung": request.data["meldung"],
    }


    #Instanziere alle nötigen Attribute für einen Heartbeat
    license = Lizenz.objects.get(license_key=beat["lizenzschluessel"])

    kundeSoftware = license.KundeHatSoftware
    datum = datetime.datetime.now()

    Heartbeat.objects.create(kundeSoftware=kundeSoftware, lizenzschluessel=beat["lizenzschluessel"],
                             meldung=beat["meldung"],
                             datum=datum)
    return Response(beat["lizenzschluessel"])



@api_view(["POST"])
def lizenzHeartbeat(request):
    """
    REST-API die zum Empfangen aller Lizenz-Requests dient.

    Das Lizenz-Request muss aus dem Lizenzschlüssel der Software bestehen.
    Bei Eingang eines Requests werden anhand des empfangenen Lizenznschlüssels das Lizenz-Objekt aus der Datenbank gefiltert,
    der dazugehörige Software-Paket ermittelt und der aktuelle sowie der neue Lizenzschlüssel unter dem Attribut replace_key notiert,
    um mit all diesen Daten den neuen Lizenzschlüssel an den Client zu senden.

    Als Response wird der neue Lizenzschlüssel zurück gegeben.

    Parameters:
        request (JSON):                Der HTTP Request des Clients in welchem sich der lizenzschluessel befindet

    Returns:
        Response (JSON):                Der neue Lizenzschlüssel wird im Response zurückgesendet
    """
    beat = {
        "lizenzschluessel": request.data["lizenzschluessel"]
    }


    #Instanziere alle nötigen Attribute für einen Heartbeat
    license = Lizenz.objects.get(license_key=beat["lizenzschluessel"])

    kundeSoftware = license.KundeHatSoftware
    datum = datetime.date.today()
    enddate = license.gültig_bis

    if enddate < datum and license.replace_key:
        return JsonResponse(json.dumps({"lizenz" : license.replace_key.license_key, "exist": True}), safe=False)

    elif enddate > datum or license.replace_key == None:
        return JsonResponse(json.dumps({"lizenz": "", "exist": False}), safe=False)


    Heartbeat.objects.create(kundeSoftware=kundeSoftware, lizenzschluessel=beat["lizenzschluessel"],
                             meldung=beat["meldung"],
                             datum=datum)
    return Response(beat["lizenzschluessel"])



# API für das überschreiben der Lizenzen
@api_view(["POST"])
def lizenzSave(request):
    """
    REST-API die zum Empfangen aller Lizenzüberschreibungsbestätigung dient.

    In dem Request stehen Informationen über den neuen und alten Lizenzschlüssel sowie eine Hilfsvariable (bool),
    die Aufschluss darüber gibt, ob der Cliet erfolgreich den Lizenzschlüssel aktualisiert hat oder nicht.
    Je nachdem werden auf Managment-Portal-Seite die Daten des Kunden aktualisiert.

    Als Response wird ein leeres dict zurück gegeben.

    Parameters:
        request (JSON):                Der HTTP Request des Clients in welchem sich der neue und alte lizenzschluessel und eine Hilfsvariable befinden

    Returns:
        Response (dict):                Leeres dict
    """

    if request.data["bool"] == "True":

        replace = Lizenz.objects.get(license_key=request.data["new"])
        gueltig_von = replace.gültig_von
        gueltig_bis = replace.gültig_bis

        Lizenz.objects.get(license_key=request.data["new"], replace_key=None).delete()
        Lizenz.objects.filter(license_key=request.data["old"]).update(license_key=request.data["new"], gültig_von=gueltig_von, gültig_bis=gueltig_bis, replace_key=None)



    return JsonResponse({})

