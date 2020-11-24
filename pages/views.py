from django.shortcuts import render

from heartbeat.models import Heartbeat
from .models import Kunde, KundeHatSoftware, Software, Standort, Lizenz
from django.http import JsonResponse, HttpResponse
import json


def home(request):
    context = {
        "kunde": Kunde.objects.all(),
        "software": Software.objects.all(),
        "khs": KundeHatSoftware.objects.all(),
        "heartbeats": Heartbeat.objects.all(),
    }
    return render(request, "dashboard.html", context)



def kundenprofil(request):
    id = request.GET.get('id', None)

    kunde = KundeHatSoftware.objects.get(id=id)



    context = {
        "kdNr": str(kunde.standort.kunde.id),
        "name": str(kunde.standort.name),
        "email": str(kunde.standort.email),
        "telNr": str(kunde.standort.telNr),
        "software": str(kunde.software),
        "plz": str(kunde.standort.plz),
        "ort": str(kunde.standort.ort),
        "strasse": str(kunde.standort.strasse),
        "hausnr": str(kunde.standort.hausnr),
    }

    print(kunde)

    return render(request, "kundenprofil.html", context)

def kunden(request):
    context = {
        "kunde": Kunde.objects.all(),
    }
    return render(request, "kunden.html", context)


def getUser(request):
    kdNr = request.GET.get('kdNr', None)

    kunde = KundeHatSoftware.objects.filter(id=kdNr)
    kundenliste = []
    for x in kunde:
        kundenliste.append({
            "software": str(x.software),
            "name": str(x.standort.name),
            #"lizenz": str(x.lizenz),
            #"version": str(x.swId.version)
        })


    print(kundenliste)

    data = {
        "kunde": kundenliste
    }

    return JsonResponse(json.dumps(kundenliste), safe=False)

def lizenzen(request):
    context = {
        'lizenzen' : Lizenz.objects.all()
    }
    return render(request,"lizenz.html", context)
