from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from add_ons import functions
from django.utils import timezone, dateformat
from PIL import Image
from home.models import Cart, Order


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
    store = models.CharField(max_length=240, blank=True, null=True)
    # ----- content ----- #
    title = models.CharField(max_length=500, blank=True, null=True)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
#                                                                        #
class Wallet(models.Model):
    # ----- relations ----- #
    bill = models.ManyToManyField(Bill, blank=True)
    # ----- content ----- #
    balance = models.IntegerField(default=0)
    # ----- functions ----- #
    def update(self):
        self.balance = 0
        for bill in self.bill.all():
            self.balance += bill.amount
        super().save()
# ---------------------------------------------------------------------- #

# ---------------------------- Custom Data ----------------------------- #
class CustomData(models.Model):
    # ----- Technical ----- #
    has_photo = models.BooleanField(default=False)
    # ----- #
    user_token = models.CharField(max_length=24, blank=True, null=True)
    product_token = models.CharField(max_length=24, blank=True, null=True)
    theme_token = models.CharField(max_length=24, blank=True, null=True)
    # ----- #
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(null=True)
    # ----- #
    tags = models.CharField(max_length=5000, blank=True, null=True)
    # ----- media ----- #
    file_name = models.CharField(max_length=300, blank=True, null=True)
    def get_file_path(self, filename):
        return self.file_name.lower()
    content = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    # ----- content ----- #
    text_1 = models.CharField(max_length=500, blank=True, null=True)
    text_2 = models.CharField(max_length=500, blank=True, null=True)
    text_3 = models.CharField(max_length=1000, blank=True, null=True)
    text_4 = models.CharField(max_length=1000, blank=True, null=True)
    # ----- functions ----- #
    def save(self, *args, **kwargs):
        self.file_name = 'custom_photos' + '/' + dateformat.format(timezone.now(), 'Y/m/d/H/i/s') + '/' + self.user_token + '/'
    def set_tags(self):
        self.tags = ''
        if self.text_1:
            self.tags += (', ' + self.text_1)
        if self.text_2:
            self.tags += (', ' + self.text_2)
        if self.text_3:
            self.tags += (', ' + self.text_3)
        if self.text_4:
            self.tags += (', ' + self.text_4)
        super().save()
# ---------------------------------------------------------------------- #

# -------------------------------- User -------------------------------- #
class User(AbstractUser):
    # ----- Technical ----- #
    is_blacklisted = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=True)
    is_customer = models.BooleanField(default=True)
    is_provider = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    # ----- #
    tags = models.CharField(max_length=5000, blank=True, null=True)
    points = models.IntegerField(default=0)
    token = models.CharField(max_length=24, unique=True, null=True)
    store_name = models.CharField(max_length=240, unique=True, null=True)
    # ----- relations ----- #
    wallet = models.OneToOneField(
        Wallet,
        on_delete=models.PROTECT,
        null=True
    )
    cart = models.OneToOneField(
        Cart,
        on_delete=models.PROTECT,
        null=True
    )
    order = models.ManyToManyField(Order, blank=True)
    custom_data = models.ManyToManyField(CustomData, blank=True)
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
        if not self.token:
            self.token = functions.serial_number_generator(24).upper()

        self.file_name = 'profile_photos' + '/' + dateformat.format(timezone.now(), 'Y/m/d/H/i/s') + '/' + self.token + '/'

        if not self.wallet:
            new_wallet = Wallet().save()
            self.wallet = new_wallet

        if not self.cart:
            new_cart = Cart().save()
            self.cart = new_cart

        if not self.store_name:
            self.store_name = self.username

        if self.profile_photo:
            img = Image.open(self.profile_photo.path)
            if img.height > 200 or img.width > 200:
                new_img = (200, 200)
                img.thumbnail(new_img)
                img.save(self.profile_photo.path)
        super().save()
    def set_tags(self):
        self.tags = ''
        if self.first_name:
            self.tags += (', ' + self.first_name)
        if self.last_name:
            self.tags += (', ' + self.last_name)
        if self.province:
            self.tags += (', ' + self.province)
        if self.municipality:
            self.tags += (', ' + self.municipality)
        if self.phone_number:
            self.tags += (', ' + self.phone_number)
        if self.store_name:
            self.tags += (', ' + self.store_name)
        super().save()
# ---------------------------------------------------------------------- #
