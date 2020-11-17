from django.shortcuts import render
from .models import Kunde, KundeHatSoftware, Software
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.forms.models import model_to_dict
from .serializers import KundenSerializer, KHSSerializer, SoftwareSerializer
import requests
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json


def home(request):
    context = {
        "kunde": Kunde.objects.all(),
        "software": Software.objects.all(),
        "khs": KundeHatSoftware.objects.all()

    }
    return render(request, "dashboard.html", context)


#   untenstehenden TEST-Befehl auf Kundenseite integrieren in Verbindung mit cronjob im Format */10 * * * * ... (alle 10 Minuten)
#   curl -X POST -d kdNr=1;mandant=Mercedes_GmbH;software=aurep;lizenz=True localhost:8000/heartbeat
@api_view(["POST"])
def heartbeat(request):

    # serializerKunde = KundenSerializer(data=request.data)
    # if serializerKunde.is_valid():
    #    serializerKunde.save()

    beat = {
        "kdNr": request.data["kdNr"],
        #"mandant": request.data["mandant"],
        "software": request.data["software"],
        "lizenz": request.data["lizenz"],
    }

    # Filtern aller KundeHatSoftwareeinträge nach jeweiliger Kundennummer
    software = KundeHatSoftware.objects.filter(kdNr=beat["kdNr"])

    # Erfassen der jeweiligen Software ID des der Software des Kunden
    softwareId = 0
    for x in software:
        if beat["software"] == str(x.swId):
            softwareId = x.swId.id

    # Filtern des jeweiligen Kunden nach Kundennummer und Software um dann die Lizenzinformation zu aktualisieren
    KundeHatSoftware.objects.filter(kdNr=beat["kdNr"], swId=softwareId).update(lizenz=beat["lizenz"])

    # Response an den Kunden zurück vielleicht nicht notwendig
    return Response(beat["kdNr"])


def kundenprofil(request):
    context = {
        "kunde": Kunde.objects.all(),
        "software": Software.objects.all(),
        "khs": KundeHatSoftware.objects.all()

    }
    return render(request, "kundenprofil.html", context)

def kunden(request):
    context = {
        "kunde": Kunde.objects.all()

    }
    return render(request, "kunden.html", context)


def getUser(request):
    kdNr = request.GET.get('kdNr', None)

    kunde = KundeHatSoftware.objects.filter(kdNr_id=kdNr)
    kundenliste = []
    for x in kunde:
        kundenliste.append({
            "kdNr": str(x.kdNr),
            "swId": str(x.swId),
            "lizenz": str(x.lizenz),
            "version": str(x.swId.version)
        })


    print(kundenliste)

    data = {
        "kunde": kundenliste
    }

    return JsonResponse(json.dumps(kundenliste), safe=False)
