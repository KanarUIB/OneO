from django.db import models
from pages.models import KundeHatSoftware
# Create your models here.
class Heartbeat(models.Model):
    kundeSoftware = models.ForeignKey(KundeHatSoftware,on_delete=models.CASCADE)
    meldung = models.TextField()
    datum = models.DateTimeField()
