from django.urls import path, include

from heartbeat import views as heartbeat_views

urlpatterns = [
    path('post/', heartbeat_views.heartbeat, name="heartbeat"),
    #path('<int:pk>/deleteHeartbeatEntry/', heartbeat_views.deleteHeartbeatEntry, name="deleteEntry"),

]
