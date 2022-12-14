from django.db import models
from shop_manager.models import Product
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator


class Clip(models.Model):
    # --------------------------------- clip technical informations ----------------------------
    sku = models.CharField(max_length=30, blank=True, null=True)
    product_title = models.CharField(max_length=400, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    # --------------------------------- media --------------------------------------------------
    thumb = models.ImageField(upload_to='sell-manager/clip/thumb', blank=True, null=True)
    # --------------------------------- clip info  ---------------------------------------------
    en_clip_title = models.CharField(max_length=100, blank=True, null=True)
    fr_clip_title = models.CharField(max_length=100, blank=True, null=True)
    ar_clip_title = models.CharField(max_length=100, blank=True, null=True)

    value = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.type


class Collection(models.Model):
    # --------------------------------- collection technical informations ----------------------
    solidarity = models.IntegerField(default=0)
    delivery = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    # --------------------------------- media --------------------------------------------------
    thumb = models.ImageField(upload_to='sell-manager/collection/thumb', blank=True, null=True)
    # --------------------------------- info ---------------------------------------------------
    product_sku = models.CharField(max_length=30, blank=True, null=True)
    en_product_name = models.CharField(max_length=300, blank=True, null=True)
    fr_product_name = models.CharField(max_length=300, blank=True, null=True)
    ar_product_name = models.CharField(max_length=300, blank=True, null=True)
    product_option = models.CharField(max_length=300, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.en_product_name


class Cart(models.Model):
    # --------------------------------- cart technical informations ----------------------------
    ref = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    device = models.CharField(max_length=200, default='UNDEFINED')
    operating_system = models.CharField(max_length=200, default='UNDEFINED')
    ip_address = models.CharField(max_length=200, default='UNDEFINED')
    # --------------------------------- info ---------------------------------------------------
    collections = models.ManyToManyField(Collection, blank=True)

    def __str__(self):
        return self.ref


class Order(models.Model):
    # --------------------------------- order technical informations ---------------------------
    cart_ref = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    device = models.CharField(max_length=200, default='UNDEFINED')
    operating_system = models.CharField(max_length=200, default='UNDEFINED')
    ip_address = models.CharField(max_length=200, default='UNDEFINED')
    state = models.CharField(max_length=100, default='PENDING')
    # --------------------------------- client info --------------------------------------------
    collections = models.ManyToManyField(Collection, blank=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    phone = PhoneNumberField(blank=True)
    destination = models.CharField(max_length=200, blank=True, null=True)
    sub_destination = models.CharField(max_length=500, blank=True, null=True)
    # --------------------------------- order info ---------------------------------------------
    coupon_title = models.CharField(max_length=30, blank=True, null=True)
    coupon_value = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    shipping_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.cart_ref
