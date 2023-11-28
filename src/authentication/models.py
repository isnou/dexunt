from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from globals import functions
from django.utils import timezone, dateformat
from PIL import Image


# ------------------------------ Setting ------------------------------- #
# ---------------------------------------------------------------------- #


# -------------------------------- User -------------------------------- #
class User(AbstractUser):
    # ----- Technical ----- #
    is_blacklisted = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)
    # ----- #
    is_worker = models.BooleanField(default=True)
    is_panelist = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    # ----- relations ----- #
    # ----- media ----- #
    file_name = models.CharField(max_length=300, blank=True, null=True)
    def get_image_path(self, filename):
        return self.file_name.lower()
    profile_photo = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    # ----- content ----- #
    first_name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    province = models.CharField(max_length=200, blank=True, null=True)
    municipality = models.CharField(max_length=200, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    # ----- functions ----- #
    def __str__(self):
        return self.username
    def save(self, *args, **kwargs):
        self.file_name = 'profile_photos' + '/' + dateformat.format(timezone.now(), 'Y/m/d/H/i/s') + '/'
        super().save()

    # ----- variables ----- #

# ---------------------------------------------------------------------- #







