from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from add_ons import functions
from django.utils import timezone, dateformat
from PIL import Image


# ------------------------------- Title -------------------------------- #
# ----- Technical ----- #
# ----- relations ----- #
# ----- media ----- #
# ----- content ----- #
# ----- #
# ----- #
# ----- functions ----- #
#                                                                        #
# ---------------------------------------------------------------------- #


# ------------------------------ Billing ------------------------------- #
class Bill(models.Model):
    # ----- Technical ----- #
    user_token = models.CharField(max_length=24, null=True)
    # ----- content ----- #
    store = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
#                                                                        #
class Wallet(models.Model):
    # ----- Technical ----- #
    user_token = models.CharField(max_length=24, null=True)
    # ----- relations ----- #
    bill = models.ManyToManyField(Bill, blank=True)
    # ----- content ----- #
    store = models.CharField(max_length=100, blank=True, null=True)
    amount = models.IntegerField(default=0)
    # ----- functions ----- #
    def update(self):
        self.amount = 0
        for bill in self.bill.all():
            self.amount += bill.amount
        super().save()
# ---------------------------------------------------------------------- #

# ---------------------------- Custom Data ----------------------------- #
class DataFolder(AbstractUser):
    # ----- Technical ----- #
    user_token = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(null=True)
    # ----- media ----- #
    file_name = models.CharField(max_length=300, blank=True, null=True)
    def get_file_path(self, filename):
        return self.file_name.lower()
    file = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    # ----- content ----- #
    # ----- functions ----- #
# ---------------------------------------------------------------------- #

# -------------------------------- User -------------------------------- #
class User(AbstractUser):
    # ----- Technical ----- #
    is_customer = models.BooleanField(default=True)
    is_provider = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    # ----- relations ----- #
    # ----- media ----- #
    file_name = models.CharField(max_length=300, blank=True, null=True)
    def get_image_path(self, filename):
        return self.file_name.lower()
    profile_photo = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    # ----- content ----- #
    # ----- #
    # ----- #
    # ----- functions ----- #
    first_name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)



    role = models.CharField(max_length=30, verbose_name='role', default='customer')
    points = models.IntegerField(default=0)
    province = models.CharField(max_length=200, blank=True, null=True)
    municipality = models.CharField(max_length=200, blank=True, null=True)
    activated_account = models.BooleanField(default=False)
    user_token = models.CharField(max_length=24, unique=True, null=True)
    store_token = models.CharField(max_length=100, unique=True, null=True)

    wallet = models.ManyToManyField(Bill, blank=True)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.user_token:
            self.user_token = functions.serial_number_generator(24).upper()

        self.file_name = self.user_token + '/' + dateformat.format(timezone.now(), 'Y/m/d/H/i/s') + '/' + 'profile_photo'

        if self.profile_photo:
            img = Image.open(self.profile_photo.path)
            if img.height > 200 or img.width > 200:
                new_img = (200, 200)
                img.thumbnail(new_img)
                img.save(self.profile_photo.path)
        super().save()

    def update_wallet(self):
        self.amount = 0
        for bill in self.bill.all():
            self.amount += bill.amount
        super().save()
