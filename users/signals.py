from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import UserProfile

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name)

@receiver(post_save, sender=UserModel)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()