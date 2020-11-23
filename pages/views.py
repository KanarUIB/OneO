from django.shortcuts import render
from .models import Kunde, KundeHatSoftware, Software
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
