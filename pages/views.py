from django.shortcuts import render
from .models import Kunde, KundeHatSoftware, Software


def home(request):
    context = {
        "kunde": Kunde.objects.all(),
        "software": Software.objects.all(),
        "khs": KundeHatSoftware.objects.all()

    }
    return render(request, "base.html", context)
