from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_photo = models.ImageField(verbose_name='profile photo')
    role = models.CharField(max_length=30, verbose_name='role')
    client_name = models.CharField(max_length=300, blank=True, null=True)
    client_phone = PhoneNumberField(blank=True)
    points = models.IntegerField(default=0)
    province = models.CharField(max_length=200, blank=True, null=True)
    municipality = models.CharField(max_length=200, blank=True, null=True)