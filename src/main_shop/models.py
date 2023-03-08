from django.db import models
from shop_manager.models import Product
from django.core.validators import MaxValueValidator, MinValueValidator


class IntroBanner(models.Model):
    # --------------------------------- layout titles ------------------------------------------
    en_intro = models.TextField(max_length=500, blank=True, null=True)
    en_title = models.TextField(max_length=500, blank=True, null=True)
    en_description = models.TextField(max_length=500, blank=True, null=True)

    fr_intro = models.TextField(max_length=500, blank=True, null=True)
    fr_title = models.TextField(max_length=500, blank=True, null=True)
    fr_description = models.TextField(max_length=500, blank=True, null=True)

    ar_intro = models.TextField(max_length=500, blank=True, null=True)
    ar_title = models.TextField(max_length=500, blank=True, null=True)
    ar_description = models.TextField(max_length=500, blank=True, null=True)
    # --------------------------------- buttons ------------------------------------------------
    en_button = models.TextField(max_length=40, blank=True, null=True)
    fr_button = models.TextField(max_length=40, blank=True, null=True)
    ar_button = models.TextField(max_length=40, blank=True, null=True)
    # --------------------------------- additional information ---------------------------------
    link = models.TextField(max_length=500, blank=True, null=True)
    thumb = models.ImageField(upload_to='main-shop/e-shop/thumb', blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.en_title

class IntroThumb(models.Model):
    # --------------------------------- layout titles ------------------------------------------
    en_title = models.TextField(max_length=300, blank=True, null=True)
    fr_title = models.TextField(max_length=300, blank=True, null=True)
    ar_title = models.TextField(max_length=300, blank=True, null=True)
    # --------------------------------- buttons ------------------------------------------------
    en_button = models.TextField(max_length=40, blank=True, null=True)
    fr_button = models.TextField(max_length=40, blank=True, null=True)
    ar_button = models.TextField(max_length=40, blank=True, null=True)
    # --------------------------------- additional information ---------------------------------
    link = models.TextField(max_length=500, blank=True, null=True)
    thumb = models.ImageField(upload_to='main-shop/e-shop/thumb', blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.en_title

class Showcase(models.Model):
    # --------------------------------- showcase technical informations ------------------------
    type = models.CharField(max_length=50, blank=True, null=True)
    # --------------------------------- showcase titles ----------------------------------------
    en_title = models.TextField(max_length=300, blank=True, null=True)
    fr_title = models.TextField(max_length=300, blank=True, null=True)
    ar_title = models.TextField(max_length=300, blank=True, null=True)
    # --------------------------------- buttons ------------------------------------------------
    en_button = models.TextField(max_length=40, blank=True, null=True)
    fr_button = models.TextField(max_length=40, blank=True, null=True)
    ar_button = models.TextField(max_length=40, blank=True, null=True)
    # --------------------------------- additional information ---------------------------------
    link = models.TextField(max_length=500, blank=True, null=True)
    thumb = models.ImageField(upload_to='main-shop/e-shop/thumb', blank=True, null=True)
    product = models.ManyToManyField(Product, blank=True)
    rank = models.IntegerField(blank=True, null=True)
    # --------------------------------- expiration ---------------------------------------------
    day = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    def products(self):
        return "\n".join([p.en_product_title for p in self.product.all()])

    def __str__(self):
        return self.en_title
