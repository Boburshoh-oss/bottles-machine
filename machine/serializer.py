from rest_framework import serializers
from .models import *

class MachineSerializer(serializers.ModelSerializer):
    qrcode = serializers.CharField()
    class Meta:
        model = Machine
        fields = ['qrcode','kilogram']