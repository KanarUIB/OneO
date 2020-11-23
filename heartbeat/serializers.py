from django.contrib.auth.models import User, Group
from rest_framework import serializers
from pages.models import Kunde, KundeHatSoftware, Software


class KundenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kunde
        fields = '__all__'


class KHSSerializer(serializers.ModelSerializer):
    class Meta:
        model = KundeHatSoftware
        fields = '__all__'


class SoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Software
        fields = '__all__'

