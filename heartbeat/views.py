
# Create your views here.
#   untenstehenden TEST-Befehl auf Kundenseite integrieren in Verbindung mit cronjob im Format */10 * * * * ... (alle 10 Minuten)
#   curl -X POST -d kdNr=1;mandant=Mercedes_GmbH;software=aurep;lizenz=True localhost:8000/heartbeat

from .models import Heartbeat
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pages.models import Lizenz, KundeHatSoftware
import datetime
from django.utils import timezone

current_date = datetime.datetime.now()
# negativeHeartbeats = []
missingHeartbeats = []


def getCurrentHeartbeats():
    heartbeat_objs = Heartbeat.objects.all()
    currentHeartbeats = []
    for heartbeat in heartbeat_objs:
        if heartbeat.datum.date() == current_date.date():
            currentHeartbeats.append(heartbeat)
            # print(heartbeat.id)
            # print(heartbeat)
    return currentHeartbeats


"""""""""
Checks if there is a Heartbeat for the specific KundeHatSoftware kundeHatSoftware on that day.
Return True if there is a Heartbeat object or False if there is no Heartbeat object for kundeHatSoftware.
"""""""""


def checkHeartbeat(kundeHatSoftware):
    hearbeat_objs = Heartbeat.objects.filter(kundeSoftware=kundeHatSoftware)
    if hearbeat_objs is not None:
        for heartbeat in hearbeat_objs:
            if heartbeat.datum.date() == current_date.date():
                if heartbeat.kundeSoftware == kundeHatSoftware:
                    return True
    return False


"""""""""
Creates Database Entries for the missing Heartbeats after checking if there is a heartbeat
for the specific KundeHatSoftware.
"""""""""


def createMissingHeartbeats():
    kundeHatSoftware_objs = KundeHatSoftware.objects.all()
    global missingHeartbeats
    for kundeSoftware in kundeHatSoftware_objs:
        if (checkHeartbeat(kundeSoftware) == False):
            # print("hier für muss ein negatives heartbeat erstellt werden: ")
            # print(str(kundeSoftware.id) + ": " + str(kundeSoftware))
            heartbeat = Heartbeat.objects.create(kundeSoftware=kundeSoftware,
                                                 lizenzschluessel=Lizenz.objects.get(
                                                     KundeHatSoftware=kundeSoftware).license_key,
                                                 meldung="Heartbeat nicht eingetroffen",
                                                 datum=datetime.datetime.now())
    for heartbeat in getCurrentHeartbeats():
        if heartbeat.meldung == "Heartbeat nicht eingetroffen":
            missingHeartbeats.append(heartbeat)


def getErrorHeartbeats():
    heartbeat_objs = getCurrentHeartbeats()
    errorHeartbeats = []
    for heartbeat in heartbeat_objs:
        if str(heartbeat.meldung).__contains__("Error"):
            errorHeartbeats.append(heartbeat)
    return errorHeartbeats


def getMissingHeartbeats():
    global missingHeartbeat
    for heartbeat in getCurrentHeartbeats():
        if heartbeat.meldung == "Heartbeat nicht eingetroffen":
            missingHeartbeat.append(heartbeat)
    return missingHeartbeat


def getNegativeHeartbeats():
    kundeSoftware_objs = KundeHatSoftware.objects.all()
    negativeHeartbeats = []
    delta = datetime.timedelta(days=2)
    for kundeSoftware in kundeSoftware_objs:
        print("---")
        for heartbeat in Heartbeat.objects.filter(kundeSoftware=kundeSoftware).order_by('-datum'):
            if timezone.make_naive(heartbeat.datum) > current_date - delta and heartbeat.meldung == "Heartbeat nicht eingetroffen":
                negativeHeartbeats.append(heartbeat)
                print(current_date - delta)
                print(heartbeat)
                break
    negativeHeartbeats += getErrorHeartbeats()
    return negativeHeartbeats

    """""""""
def getNegativeHeartbeats():
    heartbeat_objs = getCurrentHeartbeats()
    negativeHeartbeats = []
    for heartbeat in heartbeat_objs:
        for comparedHeartbeat in heartbeat_objs:
            if heartbeat.kundeSoftware == comparedHeartbeat.kundeSoftware and heartbeat.datum_utc < comparedHeartbeat.datum_utc:
                negativeHeartbeats.append(comparedHeartbeat)
            else:
                negativeHeartbeats.append(heartbeat)
    print(negativeHeartbeats)
    return negativeHeartbeats
    """""""""


def updateNegativeHeartbeats():
    global missingHeartbeats
    global negativeHeartbeats
    currentHeartbeats = getCurrentHeartbeats()
    # print(currentHeartbeats)
    missingHeartbeats = []
    for heartbeat in currentHeartbeats:
        for negativeHeartbeat in getNegativeHeartbeats():
            if heartbeat.kundeSoftware == negativeHeartbeat.kundeSoftware:
                print("Heartbeat:")
                print(heartbeat)
                print("negativeHeartbeat:")
                print(negativeHeartbeat)


@api_view(["POST"])
def heartbeat(request):
    print("\n\n\n\nDRIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIN\n\n\n\n")
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
