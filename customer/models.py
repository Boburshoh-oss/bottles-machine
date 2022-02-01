import imp
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin , BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token
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
            phone_number=phone_number,
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
            phone_number=phone_number,
            username=username,
            password=password,
            
        )
        user.is_admin = True
        user.save(using=self._db)
        print(user.is_admin)
        return user


class User(AbstractBaseUser):
    phone_number = models.CharField(
        unique=True,
        max_length=13
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
    first_name = models.CharField(max_length=200,blank=True,null=True)
    last_name = models.CharField(max_length=200,blank=True,null=True)
    image = models.ImageField(upload_to="profile_image",blank=True,null=True)
    user = models.OneToOneField("customer.User",on_delete=models.CASCADE, related_name="user_profile")
    balance = models.FloatField(default=0)
    qrcode = models.ImageField(upload_to=qrcode_location, null=True, blank=True)
    employee_id = models.CharField(unique=True, max_length=100,blank=True,null=True)
    address = models.CharField(max_length=255,blank=True,null=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.phone_number}"
    
