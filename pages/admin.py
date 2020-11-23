from django.contrib import admin
from .models import (Kunde, Software, KundeHatSoftware, Standort,
                    Lizenz, Modul,Ansprechpartner,Kundenbetreuer,
                     Zuständigkeit)

# Register your models here.

admin.site.register(Kunde)
admin.site.register(KundeHatSoftware)
admin.site.register(Software)
admin.site.register(Standort)
admin.site.register(Lizenz)
admin.site.register(Modul)
admin.site.register(Ansprechpartner)
admin.site.register(Kundenbetreuer)
admin.site.register(Zuständigkeit)




