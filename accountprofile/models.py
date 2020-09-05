from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Package(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title


class Referral(models.Model):
    #id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    referree = models.CharField(max_length=6, null=True)

    def __str__(self):
        return self.user.username
