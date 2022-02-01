import random 
from customer.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from customer.models import Profile
import qrcode
import string 

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Profile)
def qr_code_profile(sender, instance, created, **kwargs):
    if created:
        id_number = str(random.randint(1000000, 9999999))
        S = 20
        id_number += ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)    )
        qr = generate_qrcode(id_number)
        instance.employee_id = id_number
        instance.qrcode = qr
        instance.save()


def generate_qrcode(id_number):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(id_number)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"qr/{id_number}.png")

    return f'qr/{id_number}.png'