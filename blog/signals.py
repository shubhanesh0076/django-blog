from django.db.models.signals import post_save #Import a post_save signal when a user is created
from django.contrib.auth.models import User # Import the built-in User model, which is a sender
from django.dispatch import receiver # Import the receiver
from .models import Profileinfoform, Userprofile
#from .models import Profileinfoform


@receiver(post_save, sender=User) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        Userprofile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()


@receiver(post_save, sender=User) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profileinfoform.objects.create(puser=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profileinfoform.save()


