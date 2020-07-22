from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

#For signals to work import it in under apps.py in ready function of AppsConfig

#post_save signal is sent after object is saved
# receiver is a decorator which is available in django.dispatch

@receiver(post_save,sender=User)                            # Call this when an object is saved by User model(sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
        print("Profile created")
