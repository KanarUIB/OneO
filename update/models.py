from django.db import models
from pages.models import Software

# Create your models here.
class Update(models.Model):
    update_id = models.AutoField(primary_key=True)
    version = models.CharField(max_length=15)
    software = models.ForeignKey(Software, default=None, on_delete=models.CASCADE)
    datum = models.DateTimeField()
    datei_pfad = models.CharField(max_length=300)
