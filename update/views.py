from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Update
import requests



@api_view(["POST"])
def updateChecker(request):

    updates = Update.objects.get(software=request.data["software"], version=request.data["version"])
    print(updates)

    #url =  updates.datei_pfad
    """r = requests.post(url=url, data={
        "software": updates.software.software_name,
        "version": updates.version
    })
"""
    update = {
        "software": updates.software.software_name,
        "version": updates.version,
        "pfad": updates.datei_pfad
    }

    return Response(update)

@api_view(["POST"])
def updateResource(request):

    resource = Resource.objects.get(software=request.data["software"], version=request.data["version"])
    print(resource)


    update = {
        "software": resource.software.software_name,
        "version": resource.version,
        "pfad": r
    }

    return Response(update)
