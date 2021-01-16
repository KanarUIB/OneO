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

current_date = datetime.datetime.now()
negativeHeartbeats = []
missingHeartbeats = []
errorHeartbeats = []



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
    global missingHeartbeats, errorHeartbeats
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
        if str(heartbeat.meldung).__contains__("Error"):
            errorHeartbeats.append(heartbeat)
        if heartbeat.meldung == "Heartbeat nicht eingetroffen":
            missingHeartbeats.append(heartbeat)


def getNegativeHeartbeats():
    global negativeHeartbeats
    negativeHeartbeats.append(missingHeartbeats)
    negativeHeartbeats.append(errorHeartbeats)
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



"""
def missingHeartbeatsSocket(request):

    async def hello(websocket, path):
        name = await websocket.recv()
        print(f"< {name}")

        greeting = f"Hello {name}!"

        await websocket.send(greeting)
        print(f"> {greeting}")

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
    ssl_context.load_cert_chain(localhost_pem)

    start_server = websockets.serve(
        hello, "localhost", 8000, ssl=ssl_context
    )

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

"""


