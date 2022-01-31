from customer.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from customer.models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)