from django.db import models
from shop_manager.models import Product
from django.core.validators import MaxValueValidator, MinValueValidator


class Intro(models.Model):
    # --------------------------------- layout information -------------------------------------
    color = models.CharField(max_length=50, blank=True, null=True)
    banner = models.ImageField(upload_to='main-shop/e-shop/banner', blank=True, null=True)
    fixed = models.BooleanField(default=False)
    repeat = models.BooleanField(default=False)
    margin = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.color

class Showcase(models.Model):
    # --------------------------------- showcase technical informations ------------------------
    type = models.CharField(max_length=50, blank=True, null=True)
    publish = models.BooleanField(default=False)
    sku = models.CharField(max_length=20, unique=True, null=True)
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

class Category(models.Model):
    # --------------------------------- category identification --------------------------------
    en_title = models.CharField(max_length=200, blank=True, null=True)
    fr_title = models.TextField(max_length=300, blank=True, null=True)
    ar_title = models.TextField(max_length=300, blank=True, null=True)
    # --------------------------------- technical details --------------------------------------
    rank = models.IntegerField(blank=True, null=True)
    publish = models.BooleanField(default=False)
    sku = models.CharField(max_length=20, unique=True, null=True)
    product = models.ManyToManyField(Product, blank=True)

    def products(self):
        return "\n".join([p.en_title for p in self.product.all()])

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.en_title

class SubDirectory(models.Model):
    # --------------------------------- category identification --------------------------------
    en_title = models.CharField(max_length=200, blank=True, null=True)
    fr_title = models.TextField(max_length=300, blank=True, null=True)
    ar_title = models.TextField(max_length=300, blank=True, null=True)
    # --------------------------------- technical details --------------------------------------
    rank = models.IntegerField(blank=True, null=True)
    publish = models.BooleanField(default=False)
    sku = models.CharField(max_length=20, unique=True, null=True)
    category = models.ManyToManyField(Category, blank=True)

    def categories(self):
        return "\n".join([p.en_title for p in self.category.all()])

    class Meta:
        verbose_name_plural = "SubDirectories"

    def __str__(self):
        return self.en_title

class RootDirectory(models.Model):
    # --------------------------------- category identification --------------------------------
    en_title = models.CharField(max_length=200, blank=True, null=True)
    fr_title = models.TextField(max_length=300, blank=True, null=True)
    ar_title = models.TextField(max_length=300, blank=True, null=True)
    # --------------------------------- offer details ------------------------------------------
    offer_en_title = models.CharField(max_length=200, blank=True, null=True)
    offer_fr_title = models.CharField(max_length=200, blank=True, null=True)
    offer_ar_title = models.CharField(max_length=200, blank=True, null=True)
    offer_link = models.TextField(max_length=500, blank=True, null=True)
    offer_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    # --------------------------------- technical details --------------------------------------
    rank = models.IntegerField(blank=True, null=True)
    publish = models.BooleanField(default=False)
    sku = models.CharField(max_length=20, unique=True, null=True)
    sub_directory = models.ManyToManyField(SubDirectory, blank=True)
    # --------------------------------- media --------------------------------------------------
    thumb = models.ImageField(upload_to='main-shop/e-shop/category/', blank=True, null=True)


    def sub_directories(self):
        return "\n".join([p.en_title for p in self.sub_directory.all()])

    class Meta:
        verbose_name_plural = "RootDirectories"

    def __str__(self):
        return self.en_title
