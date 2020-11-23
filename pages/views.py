from django.shortcuts import render
from .models import Kunde, KundeHatSoftware, Software, Standort
from django.http import JsonResponse, HttpResponse
import json


def home(request):
    context = {
        "kunde": Kunde.objects.all(),
        "software": Software.objects.all(),
        "khs": KundeHatSoftware.objects.all()

    }
    return render(request, "dashboard.html", context)



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

    kunde = Standort.objects.filter(id=kdNr)
    kundenliste = []
    for x in kunde:
        kundenliste.append({
            "id": str(x.id),
            "swId": str(x.name),
            #"lizenz": str(x.lizenz),
            #"version": str(x.swId.version)
        })


    print(kundenliste)

    data = {
        "kunde": kundenliste
    }

    return JsonResponse(json.dumps(kundenliste), safe=False)
