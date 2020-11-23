from django.db import models

# Create your models here.
class Update(models.Model):
    update_id = models.AutoField(primary_key=True)
    version = models.CharField(max_length=15)
    datum = models.DateTimeField()
    datei_pfad = models.CharField(max_length=300)
