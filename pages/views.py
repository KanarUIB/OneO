from django.shortcuts import render
from .models import Kunde, KundeHatSoftware, Software
from django.http import JsonResponse, HttpResponse
from django.core import serializers


def home(request):
    context = {
        "kunde": Kunde.objects.all(),
        "software": Software.objects.all(),
        "khs": KundeHatSoftware.objects.all()

    }
    return render(request, "extends.html", context)


def getUser(request):
    kdNr = request.GET.get('kdNr', None)

    kunde = KundeHatSoftware.objects.filter(kdNr_id=kdNr).values('kdNr', 'swId', 'lizenz')
    #kunde = serializers.serialize('json', KundeHatSoftware.objects.filter(kdNr_id=kdNr), fields=('kd','size'))

    data = {
        #'kdNr': list(KundeHatSoftware.objects.filter(id=kdNr).values_list("id", "kdNr", "swId", "lizenz")),
        "kunde": kunde
    }

    return HttpResponse(data)
