from django.contrib.auth.models import User, Group
from rest_framework import serializers
from pages.models import Kunde, KundeHatSoftware, Software
from .models import Heartbeat

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

class HeartbeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heartbeat
        fields = '__all__'

#class LizenzSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Lizenz
#        fields = '__all__'
