from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin , BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token
import random
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, phone_number, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone_number:
            raise ValueError('Users must have an phone number')
        if not username:
            raise ValueError('Users must have an username')
        
        user = self.model(
            phone_number=self.phone_number,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            phone_number,
            username=username,
            password=password,
            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    phone_number = PhoneNumberField(
        unique=True
    )
    username = models.CharField(max_length=200, unique=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    # EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']
        
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    @property
    def token(self):
        try:
            token = Token.objects.get(user=self)
        except Token.DoesNotExist:
            token = Token.objects.create(user=self)
        return token.key

def upload_location(instance, filename):
    return '%s/profile_images/%s/' % (instance.user.username, filename)


def qrcode_location(instance, filename):
    return '%s/qr_codes/%s/' % (instance.user.username, filename)

class Profile(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="profile_image")
    user = models.OneToOneField("customer.User",on_delete=models.CASCADE, related_name="user_profile")
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    qrcode = models.ImageField(upload_to=qrcode_location, null=True, blank=True)
    employee_id = models.CharField(unique=True, max_length=11)
    address = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username}"
    
    def save(self):
        first_initial = self.first_name[0].upper()
        second_initial = self.last_name[0].upper()
        id_number = first_initial + second_initial + str(random.randint(1000000, 9999999))
        self.generate_qrcode()

        if not Profile.objects.filter(employee_id=id_number).exists():
            self.employee_id = id_number
            super(Profile, self).save()



    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data('Some data')
        qr.make(fit=True)

        filename = 'qrcode-code1.png'

        img = qr.make_image()
        img.save('media_cdn/' + qrcode_location(self, filename))