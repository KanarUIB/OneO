from django.urls import path, include

from heartbeat import views as heartbeat_views
from . import views

urlpatterns = [
    path('', views.home, name="index"),
    path('Kunden/Profil/<int:id>/', views.kundenprofil, name="kundenprofil"),
    path('Kunden/', views.kunden, name="kunden"),
    path('Kunden/create/', views.create_kunde, name="create_kunde"),
    path('Kunden/Profil/<int:id>/create_standort/', views.create_standort, name="create_standort"),
    path('Kunden/Profil/<int:id>/create_software/', views.create_software, name="create_software"),
    path('Kunden/Profil/<int:id>/update_license/', views.update_license, name="update_license"),

]
