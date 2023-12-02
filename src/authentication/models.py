from django.db import models
from django.utils import timezone, dateformat
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
#from PIL import Image
from globals.functions import serial_number_generator
from globals.functions import text_selector


# ------------------------------ Setting ------------------------------- #
class Transaction(models.Model):
    # ----- Technical ----- #
    currency = models.CharField(max_length=50, default='blank', null=True)
    # dzd | dxpt #
    secret_key = models.CharField(max_length=10, blank=True, unique=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    # ----- relations ----- #
    user = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE, related_name='transactions', blank=True, null=True)
    # ----- content ----- #
    note = models.CharField(max_length=500, blank=True, null=True)
    amount = models.IntegerField(default=0)
    add = models.BooleanField(default=True)
    # ----- functions ----- #
    def __str__(self):
        return self.note
    def save(self, *args, **kwargs):
        super().save()
    def generate_secret_key(self):
        self.secret_key = serial_number_generator(10)
        super().save()
    # ----- variables ----- #
    def ref(self):
        return str(self.id+1).zfill(10)
# ---------------------------------------------------------------------- #


# -------------------------------- User -------------------------------- #
class User(AbstractUser):
    # ----- Technical ----- #
    type = models.CharField(max_length=50, default='blank', null=True)
    # worker | panelist | member #
    is_blacklisted = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)
    # ----- relations ----- #

    # ----- media ----- #
    def get_image_path(self):
        return 'profile_photos/' + self.type + '/' + dateformat.format(timezone.now(), 'Y/m/d/H/i/s') + '/'
    profile_photo = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    # ----- content ----- #
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    personal_id_number = models.CharField(max_length=40, unique=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    # ----- functions ----- #
    def __str__(self):
        return self.username
    def save(self, *args, **kwargs):
        if kwargs.get('type', None):
            if kwargs.get('type') == 'worker':
                self.type = 'worker'
            if kwargs.get('type') == 'panelist':
                self.type = 'panelist'
            if kwargs.get('type') == 'member':
                self.type = 'member'
        super().save()
    # ----- variables ----- #
    def status(self):
        if self.type == 'blank':
            show = text_selector(
                en_text="Not Complete",
                fr_text="Non Achevé",
                ar_text="غير مكتمل",
            )
            return {
                'show': show,
                'color': 'danger',
            }
        # désactivé/ غير مفعل /disabled




# ---------------------------------------------------------------------- #







