from django.db import models
from pages.models import KundeHatSoftware
# Create your models here.
class Heartbeat(models.Model):
    kundeSoftware = models.ForeignKey(KundeHatSoftware,on_delete=models.CASCADE)
    lizenzschluessel = models.TextField(max_length=200, null=True, blank=True, default=None)
    meldung = models.TextField()
    datum = models.DateTimeField()

    def __str__(self):
        return str(self.kundeSoftware) + ':' + str(self.datum)


