from rest_framework import serializers

class Kunde(serializers.ModelSerializer):
    class Meta:
        model = Kunde
        fileds = "__all__"