from django.urls import path, include

from heartbeat import views as heartbeat_views
from . import views

urlpatterns = [
    path('', views.home, name="index"),
    path('Kunden/Profil', views.kundenprofil, name="kundenprofil"),
    path('Kunden/', views.kunden, name="kunden"),
    # path('getUser/', views.getUser, name='getUser'),
]
