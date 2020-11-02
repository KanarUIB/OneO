from django.contrib import admin
from .models import Kunde, Software, KundeHatSoftware

# Register your models here.

admin.site.register(Kunde)
admin.site.register(KundeHatSoftware)
admin.site.register(Software)

