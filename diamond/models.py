from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image
from accountprofile.models import Package

import uuid
import base64
from django.utils.crypto import get_random_string

code = get_random_string(5).upper()  # random cod


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    photo = models.ImageField(upload_to='user/', default='true.jpg')
    bankname = models.CharField(max_length=200, default='')
    bankacc = models.CharField(max_length=100, default='')
    accountname = models.CharField(max_length=100, default='')
    points = models.CharField(max_length=100, default=1)
    paid = models.BooleanField(default=False)
    referral_code = models.CharField(max_length=6, default=code)
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, default=True)

    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    def save(self):
        super().save()

        img = Image.open(self.photo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)


def create_profile(sender,  **kwargs):
    if kwargs['created']:
        user_profile = UserProfile(user=kwargs['instance'])
        user_profile.save()


post_save.connect(create_profile, sender=User)
