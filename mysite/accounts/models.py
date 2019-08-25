from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    email = models.EmailField(default='')
    bt_id = models.CharField(max_length=50, default='0')
    subscription_id = models.CharField(max_length=50, default='0')
    status = models.CharField(max_length=50, default='0')




def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user = kwargs['instance'])


post_save.connect(create_profile, sender=User)
