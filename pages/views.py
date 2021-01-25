from django.shortcuts import render, redirect
import heartbeat.views as heartbeat_views
from heartbeat.models import Heartbeat
from .forms import StandortCreateForms, KundeCreateForms, SoftwareCreateForm, \
    StandortlizenzCreateForm
from .models import Kunde, KundeHatSoftware, Software, Standort, Lizenz, Ansprechpartner, Modul, Standortlizenz
from django.http import HttpResponse
import datetime
from django.core.exceptions import ObjectDoesNotExist


def getAmountUser():
    """
        Sammelt die Nutzerzahlen für alle vorhandenen Softwares in einer Liste
        @return List Liste aller Software-Nutzerzahlen
    """

    softwareUsers = []
    for software in Software.objects.all():
        softwareUsers.append(len(KundeHatSoftware.objects.filter(software=software)))
    return softwareUsers


def getLicenseDeltaDays():
    """
        Gibt eine Liste mit der Menge an Lizenzen die in den nächsten 30 Tagen, +30 Tagen oder 90 Tagen ablaufen werden.
        Die Zahlen werden wie in der oben genannten Reihenfolge in die Liste hiznugefügt und wiedergeben.

        @return List Menge der bald ablaufenden Lizenzen
    """

    lizenzen = Lizenz.objects.all()
    licenseDeltaDays = []
    oneMonth = 0
    threeMonth = 0
    others = 0
    for lizenz in lizenzen:
        tage_uebrig = lizenz.gültig_bis - datetime.date.today()
        if tage_uebrig.days <= 30:
            oneMonth += 1
        elif tage_uebrig.days <= 90:
            threeMonth += 1
        else:
            others += 1
    licenseDeltaDays.append(oneMonth)
    licenseDeltaDays.append(threeMonth)
    licenseDeltaDays.append(others)
    return licenseDeltaDays


def home(request):
    """
        Antwortet auf den Aufruf der Index-Seite mit den im context genannten Informationen und triggert
        die chechHeartbeat()-Methode, welches prüft, ob es ausstehende Heartbeats gibt.
        @return render Gibt Dashboardseite mit den jeweiligen context Informationen aus.
    """

    heartbeat_views.checkHeartbeat()
    context = {
        "kunde": Kunde.objects.all(),
        "softwares": Software.objects.all(),
        "khs": KundeHatSoftware.objects.all(),
        "heartbeats": heartbeat_views.getNegativeHeartbeats(),
        "lizenzenDelta": getLicenseDeltaDays(),
        "anzahlKunden": getAmountUser(),
    }
    return render(request, "dashboard.html", context)


def kundenprofil(request, id):
    """
        Wird bei Aufruf der Kundenprofilseite aufgerufen.

        Entnimmt aus dem Request die in der Domain übergebene Kunden ID und sucht in der Datenbank nach dem Kunden und all
        seinen Standorten.
        Wenn die ID ungültig sein oder kein Kunden-Objekt für diese ID hinterlegt sein wird eine 404-Seite zurück gegeben.
        Bei Erfolg wird durch den context alle Informationen zum Kunden, seinen Standorten, seiner genutzten Softwares und
        die dazugehörigen Heartbeats weitergegeben.

        @return render Gibt die Kundenprofilseite ausgefüllt mit den jeweiligen Kundeninformationen aus.
    """

    try:
        kunde = Kunde.objects.get(id=str(id))
        kundenStandorte = Standort.objects.filter(kunde=kunde)
        print(kundenStandorte)
    except ObjectDoesNotExist:
        return render(request, "404.html")

    if id is None or not kunde:
        return HttpResponse("404.html")

    if id is not None:
        context = {
            "kunde": kunde,
            "standorte": kundenStandorte,
            "softwarePakete": getStandortSoftware(kundenStandorte),
            "standortBerater": Ansprechpartner.objects.all(),
            "softwareLizenzen": Lizenz.objects.all(),
            "heartbeatHistorie": heartbeatHistorie(getStandortSoftware(kundenStandorte)),
            "softwares": Software.objects.all(),
            "module": Modul.objects.all(),
        }

    return render(request, 'kundenprofil.html', context)


def kunden(request):
    """
        Wird bei Aufruf der Kundenseite aufgerufen.
        Gibt durch den context alle in der Datenbank aufgefundenen Kunden zurück.

        @return render Die Kundenseite mit allen in der Datenbank aufgefunden Kunden
    """

    context = {
        "kunde": Kunde.objects.all(),
    }
    return render(request, "kunden.html", context)


def lizenzen(request):
    """"
        Wird bei Aufruf der Lizenzseite aufgerufen.
        Gibt durch den context alle in der Datenbank aufgefundenen Linzenzen zurück.

        @return render Die Lizenzseite mit allen in der Datenbank aufgefunden Lizenzen
    """

    context = {
        'lizenzen': Lizenz.objects.all(),
    }
    return render(request, "lizenz.html", context)


def updates(request):
    """
        Wird bei Aufruf der Updateseite aufgerufen.
        Gibt durch den context alle in der Datenbank aufgefundenen Lizenzen und Softwares zurück.

        @return render Die Updateseite mit allen in dem context angegebenen Informationen
    """

    context = {
        'lizenzen': Lizenz.objects.all(),
        'softwares': Software.objects.all()
    }
    return render(request, 'updates.html', context)


def getStandortSoftware(standorte):
    """
        Gibt alle Software-Pakete die, der im Parameter übergebenen Standorte, gehören in einer Liste zurück.

        @return List Liste aller Software-Pakete eller Standorte aus dem Parameter
        @param standort Ein spezifischer Standort eines Kunden
    """

    softwareVonKunde = []

    for standort in standorte:
        for software in KundeHatSoftware.objects.filter(standort=standort):
            softwareVonKunde.append(software)

    return softwareVonKunde


def heartbeatHistorie(softwarePakete):
    """
        Gibt alle Heartbeats der im Parameter übergebenen Software-Pakete zurück.

        @param softwarePakete
        @return List Liste aller Heartbeats der übergebenen Software-Pakete
    """

    heartbeat_historie = []

    for paket in softwarePakete:
        for heartbeat in Heartbeat.objects.filter(kundeSoftware=paket):
            heartbeat_historie.append(heartbeat)

    return heartbeat_historie


def create_kunde(request):
    anz = int(request.POST.get("anzahlStandorte"))
    dataKunde = {
        "name": request.POST.get("name"),
        "vf_nummer": request.POST.get("vf_nummer"),
    }

    formKunde = KundeCreateForms(dataKunde)

    if request.method == 'POST':
        if formKunde.is_valid():
            formKunde.save()
            kunde = Kunde.objects.get(name=dataKunde["name"])
            for z in range(0, anz):
                dataStandort = {
                    "kunde": kunde,
                    "name": request.POST.getlist("standort[]")[z],
                    "plz": request.POST.getlist("plz[]")[z],
                    "ort": request.POST.getlist("ort[]")[z],
                    "strasse": request.POST.getlist("strasse[]")[z],
                    "hausnr": request.POST.getlist("hausnr[]")[z],
                    "email": request.POST.getlist("email[]")[z],
                    "telNr": request.POST.getlist("telNr[]")[z],
                }
                formStandort = StandortCreateForms(dataStandort)
                if formStandort.is_valid():
                    formStandort.save()

    return redirect('kunden')


def create_standort(request, id):
    kunde = Kunde.objects.get(id=id)
    form = StandortCreateForms()
    if request.method == 'POST':
        formData = {
            "kunde": kunde,
            "name": request.POST.get("name"),
            "plz": request.POST.get("plz"),
            "ort": request.POST.get("ort"),
            "strasse": request.POST.get("strasse"),
            "hausnr": request.POST.get("hausnr"),
            "email": request.POST.get("email"),
            "telNr": request.POST.get("telNr"),
        }
        form = StandortCreateForms(formData)
        if form.is_valid():
            form.save()
            return redirect('kundenprofil', id)
    context = {
        'form': form,
    }
    return redirect('kundenprofil', id)


"""""
Wird beim hinzufügen von einem 

"""""


def create_software(request, id):
    modul = Modul.objects.get(name=request.POST.get("modul"))
    if request.method == "POST":

        standort = Standort.objects.get(id=request.POST.get("standort"))
        softwarePaketData = {
            "standort": standort,
            "software": modul.produkt,
            "version": request.POST.get("version")
        }
        softwareForm = SoftwareCreateForm(softwarePaketData)
        if softwareForm.is_valid():

            softwareForm.save()
            softwarePaket = KundeHatSoftware.objects.last()

            lizenzData = {
                "KundeHatSoftware": softwarePaket,
                "modul": modul,
                "license_key": request.POST.get("license_key"),
                "detail": request.POST.get("detail"),
                "gültig_von": request.POST.get("gültig_von"),
                "gültig_bis": request.POST.get("gültig_bis"),
                "standort_id": standort.id,
            }
            lizenzForm = StandortlizenzCreateForm(lizenzData)
            if lizenzForm.is_valid():
                lizenzForm.save()
            return redirect('kundenprofil', id)
    return redirect('kundenprofil', id)


def update_license(request, id):
    alteLizenzObj = Standortlizenz.objects.get(license_key=request.POST.get("alteLizenz"))
    if request.method == "POST":
        lizenzData = {
            "KundeHatSoftware": alteLizenzObj.KundeHatSoftware,
            "modul": alteLizenzObj.modul,
            "license_key": request.POST.get("license_key"),
            "detail": request.POST.get("detail"),
            "gültig_von": request.POST.get("gültig_von"),
            "gültig_bis": request.POST.get("gültig_bis"),
            "replace_key": alteLizenzObj,
            "standort_id": alteLizenzObj.standort_id,
        }
        lizenzForm = StandortlizenzCreateForm(lizenzData)
        if lizenzForm.is_valid():
            lizenzForm.save()
            Standortlizenz.objects.filter(id=alteLizenzObj.id).update(
                detail="[Neue Lizenz vorhanden]")
            return redirect('kundenprofil', id)

    return redirect('kundenprofil', id)
