from django.shortcuts import get_object_or_404, render
from .models import *
from rest_framework import generics
from .serializer import * 
from customer.models import *
money_for_kg = 1000

class MachineView(generics.CreateAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

    def perform_create(self, serializer):
        money = float(serializer.validated_data['kilogram']) * money_for_kg
        profile = get_object_or_404(Profile,employee_id = str(serializer.validated_data['qrcode']))
        profile.balance += money
        profile.save()
        user = profile.user
        serializer.save(money = money,profile = user)
        return super().perform_create(serializer)
