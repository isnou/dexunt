from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from sell_manager.models import Order, UserCart
from main_shop.models import WishedProduct, NotifiedProduct, Server
from PIL import Image


class User(AbstractUser):
    # --------------------------------- user info ----------------------------------------------
    first_name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True)
    profile_photo = models.ImageField(verbose_name='profile photo')
    role = models.CharField(max_length=30, verbose_name='role', default='CUSTOMER')
    points = models.IntegerField(default=0)
    province = models.CharField(max_length=200, blank=True, null=True)
    municipality = models.CharField(max_length=200, blank=True, null=True)
    activated_account = models.BooleanField(default=False)

    # --------------------------------- user activities ----------------------------------------
    order = models.ManyToManyField(Order, blank=True)
    cart = models.ManyToManyField(UserCart, blank=True)
    server = models.ManyToManyField(Server, blank=True)
    wished_product = models.ManyToManyField(WishedProduct, blank=True)
    notified_product = models.ManyToManyField(NotifiedProduct, blank=True)

    def save(self, *args, **kwargs):
        super().save()

        if open(self.profile_photo):
            img = Image.open(self.profile_photo.path)
            if img.height > 200 or img.width > 200:
                new_img = (200, 200)
                img.thumbnail(new_img)
                img.save(self.profile_photo.path)

