from django.shortcuts import render
from .models import Kunde, KundeHatSoftware, Software
from django.http import JsonResponse


def home(request):
    context = {
        "kunde": Kunde.objects.all(),
        "software": Software.objects.all(),
        "khs": KundeHatSoftware.objects.all()

    }
    return render(request, "extends.html", context)

def getUser(request):
    kdNr = request.GET.get('kdNr', None)
    data = {
        'kdNr': KundeHatSoftware.objects.filter(kdNr__iexact=kdNr).exists()
    }
    return JsonResponse(data)


