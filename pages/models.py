from django.db import models
import datetime


class Kunde(models.Model):
    mandant = models.CharField(max_length=50)

    def __str__(self):
        return str(self.mandant)

    def equals(self, string):
        return self.mandant == string


class Standort(models.Model):
    kunde = models.ForeignKey(Kunde, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    telNr = models.CharField(max_length=50)
    email = models.EmailField()
    strasse = models.CharField(max_length=100)
    hausnr = models.CharField(max_length=5)
    plz = models.CharField(max_length=10)
    ort = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Software(models.Model):
    software_name = models.CharField(max_length=50)
    version = models.CharField(max_length=10, default="NULL")
    beschreibung = models.TextField(default="")

    def __str__(self):
        return self.software_name


class KundeHatSoftware(models.Model):
    standort = models.ForeignKey(Standort, on_delete=models.CASCADE)
    software = models.ForeignKey(Software, on_delete=models.CASCADE)
    # lizenz = models.BooleanField(default=False)
    version = models.CharField(max_length=10)

    def __str__(self):
        return self.standort.kunde.mandant + " - " + self.standort.ort + ": " + self.software.software_name


#   return "Kundennummer: " + self.kdNr + ", Software-Id: " + self.swId + ", Aktive Lizenz?: " + self.lizenz


class Modul(models.Model):
    name = models.CharField(max_length=50)
    produkt = models.ForeignKey(Software, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lizenz(models.Model):
    KundeHatSoftware = models.ForeignKey(KundeHatSoftware, on_delete=models.CASCADE)
    modul = models.ForeignKey(Modul, on_delete=models.CASCADE)
    license_key = models.CharField(max_length=300)
    detail = models.TextField()
    gültig_von = models.DateField(auto_now_add=False, auto_now=False, blank=True)
    gültig_bis = models.DateField(auto_now_add=False, auto_now=False, blank=True)

    def __str__(self):
        return self.KundeHatSoftware.__str__() + " - " + self.modul.name


class Person(models.Model):
    vorname = models.CharField(max_length=100)
    nachname = models.CharField(max_length=100)
    telefon_nr = models.CharField(max_length=50)
    email = models.EmailField()

    class Meta:
        abstract = True


class Ansprechpartner(Person):
    standort = models.ForeignKey(Standort, on_delete=models.CASCADE)
    zuständige_software = models.ManyToManyField(
        Software,
        through='Zuständigkeit',
        through_fields=('ansprechpartner', 'software'),
    )


class Zuständigkeit(models.Model):
    ansprechpartner = models.ForeignKey(Ansprechpartner, on_delete=models.SET_NULL,
                                        blank=True, null=True)
    software = models.ForeignKey(Software, on_delete=models.SET_NULL,
                                 blank=True, null=True)


class Kundenbetreuer(Person):
    pass
