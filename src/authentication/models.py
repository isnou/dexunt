from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True)
    profile_photo = models.ImageField(verbose_name='profile photo')
    role = models.CharField(max_length=30, verbose_name='role', default='CUSTOMER')
    points = models.IntegerField(default=0)
    province = models.CharField(max_length=200, blank=True, null=True)
    municipality = models.CharField(max_length=200, blank=True, null=True)
    activated_account = models.BooleanField(default=False)
    first_connection = models.BooleanField(default=True)