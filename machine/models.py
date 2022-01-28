from django.db import models
from customer.models import User
# Create your models here.

class Machine(models.Model):
    kilogram = models.CharField(max_length=7)
    money = models.CharField(max_length=50)
    profile = models.OneToOneField(User,on_delete=models.CASCADE)
    qrcode = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.profile} {self.kilogram}"