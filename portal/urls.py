"""portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pages import views as page
from django.contrib.auth import views as auth_views
from users import views as user_views
from update import views as update_views
from heartbeat import views as heartbeat_view
import datetime
import asyncio
import asyncws
import random
import websockets

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    # path('', page.home, name="index"),
    path('', include("pages.urls")),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', user_views.register, name='register'),
    path('updates/', page.updates, name='updates'),
    path('updates/updateChecker', update_views.updateChecker, name='updateChecker'),
    path('getUser/', page.getUser, name="getUser"),
    path('lizenzen/', page.lizenzen, name='lizenzen'),
    path('update/', page.updates, name='update'),
    path('heartbeat', heartbeat_view.heartbeat, name="heartbeat")
]


"""
async def time(websocket, path):
    print("test")
    while True:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        await websocket.send(now)
        await asyncio.sleep(random.random() * 3)


start_server = websockets.serve(time, "127.0.0.1", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
"""