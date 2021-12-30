from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.utils import timezone
import json


class ClientProfile(models.Model):
    user_p = models.OneToOneField(User, on_delete=models.CASCADE)

    name_p = models.CharField(max_length=100, default="nameNotSet")
    image_p = models.ImageField(default=r'profile_pic/defaultNew.jpg', upload_to='profile_pic')
    address_p = models.TextField(max_length=250)
    phone_p = models.CharField(max_length=20)

    # */*/*
    since_cp = models.TimeField(default=timezone.now)


class WorkerProfile(models.Model):
    user_p = models.OneToOneField(User, on_delete=models.CASCADE)

    name_p = models.CharField(max_length=100)
    image_p = models.ImageField(default=r'profile_pic/defaultNew.jpg', upload_to='profile_pic')
    address_p = models.TextField(max_length=250)
    phone_p = models.CharField(max_length=20)

    # */*/*
    role_wp = ArrayField(models.CharField(max_length=10, blank=True, choices=
                [(class_obj, class_obj) for class_obj in json.load(open(r"DB/etc/roles.json"))]))
    time_available_wp = ArrayField(models.CharField(max_length=10, blank=True))
