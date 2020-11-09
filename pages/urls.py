from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="index"),
    #path('getUser/', views.getUser, name='getUser'),

]
