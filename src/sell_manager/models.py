from django.db import models
from shop_manager.models import Product
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator


class CartProduct(models.Model):
    # --------------------------------- collection technical informations ----------------------
    delivery = models.IntegerField(default=100)
    points = models.IntegerField(default=0)
    # --------------------------------- media --------------------------------------------------
    thumb = models.ImageField(upload_to='sell-manager/collection/thumb', blank=True, null=True)
    # --------------------------------- info ---------------------------------------------------
    product_sku = models.CharField(max_length=30, blank=True, null=True)
    size_sku = models.CharField(max_length=30, blank=True, null=True)

    en_name = models.CharField(max_length=300, blank=True, null=True)
    fr_name = models.CharField(max_length=300, blank=True, null=True)
    ar_name = models.CharField(max_length=300, blank=True, null=True)

    en_spec = models.CharField(max_length=300, blank=True, null=True)
    fr_spec = models.CharField(max_length=300, blank=True, null=True)
    ar_spec = models.CharField(max_length=300, blank=True, null=True)

    en_detail = models.CharField(max_length=300, blank=True, null=True)
    fr_detail = models.CharField(max_length=300, blank=True, null=True)
    ar_detail = models.CharField(max_length=300, blank=True, null=True)

    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.en_name


class Cart(models.Model):
    # --------------------------------- cart technical informations ----------------------------
    ref = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    device = models.CharField(max_length=200, default='UNDEFINED')
    operating_system = models.CharField(max_length=200, default='UNDEFINED')
    ip_address = models.CharField(max_length=200, default='UNDEFINED')
    # --------------------------------- info ---------------------------------------------------
    product = models.ManyToManyField(CartProduct, blank=True)
    sub_total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.ip_address


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
    product = models.ManyToManyField(CartProduct, blank=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    phone = PhoneNumberField(blank=True)
    destination = models.CharField(max_length=200, blank=True, null=True)
    sub_destination = models.CharField(max_length=200, blank=True, null=True)
    full_address = models.CharField(max_length=500, blank=True, null=True)
    # --------------------------------- order info ---------------------------------------------
    coupon_title = models.CharField(max_length=30, blank=True, null=True)
    coupon_value = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    shipping_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.cart_ref

class SubDestination(models.Model):
    # --------------------------------- shipping details ---------------------------------------
    name = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name

class Destination(models.Model):
    # --------------------------------- shipping details ---------------------------------------
    name = models.CharField(max_length=200, blank=True, null=True)
    sub_destination = models.ManyToManyField(SubDestination, blank=True)

    def __str__(self):
        return self.name
