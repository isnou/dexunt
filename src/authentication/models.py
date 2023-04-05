from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_photo = models.ImageField(verbose_name='profile photo')
    role = models.CharField(max_length=30, verbose_name='role')
    banned = models.BooleanField(default=False)