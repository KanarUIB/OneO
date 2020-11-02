from django.db import models
import datetime


class Kunde(models.Model):
    mandant = models.CharField(max_length=50)

    def __str__(self):
        return str(self.mandant)

    def equals(self, string):
        return self.mandant == string




class KundeHatSoftware(models.Model):
    kdNr = models.ForeignKey("Kunde", on_delete=models.CASCADE)
    swId = models.ForeignKey("Software", on_delete=models.CASCADE)
    lizenz = models.BooleanField(default=False)

    #def __str__(self):
     #   return "Kundennummer: " + self.kdNr + ", Software-Id: " + self.swId + ", Aktive Lizenz?: " + self.lizenz


class Software(models.Model):
    software = models.CharField(max_length=50)
    version = models.CharField(max_length=10, default="NULL")
    beschreibung = models.TextField(default="")

    def __str__(self):
        return self.software
