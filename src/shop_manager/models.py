from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class Feature(models.Model):
    # --------------------------------- feature types ------------------------------------------
    en_title = models.CharField(max_length=150, blank=True, null=True)
    fr_title = models.CharField(max_length=150, blank=True, null=True)
    ar_title = models.CharField(max_length=150, blank=True, null=True)
    # --------------------------------- feature value ------------------------------------------
    en_value = models.TextField(max_length=500, null=True)
    fr_value = models.TextField(max_length=500, null=True)
    ar_value = models.TextField(max_length=500, null=True)

    def __str__(self):
        return self.en_title


class Album(models.Model):
    file_name = models.CharField(max_length=500, blank=True, default='product-image')
    image = models.ImageField(upload_to='shop-manager/product/images/')

    class Meta:
        verbose_name_plural = "Album"

    def __str__(self):
        return self.file_name


class Product(models.Model):
    # --------------------------------- product identification en ------------------------------
    en_title = models.CharField(max_length=200, blank=True, null=True)
    en_variant = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- product identification fr ------------------------------
    fr_title = models.CharField(max_length=200, blank=True, null=True)
    fr_variant = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- product identification ar ------------------------------
    ar_title = models.CharField(max_length=200, blank=True, null=True)
    ar_variant = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- media --------------------------------------------------
    thumb = models.ImageField(upload_to='shop-manager/product/thumb', blank=True, null=True)
    album = models.ManyToManyField(Album, blank=True)
    # --------------------------------- technical details --------------------------------------
    publish = models.BooleanField(default=True)
    type = models.CharField(max_length=80, blank=True, null=True)
    upc = models.CharField(max_length=20, unique=True, null=True)
    sku = models.CharField(max_length=20, unique=True, null=True)
    tag = models.CharField(max_length=500, blank=True, default='tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    review_rate = models.IntegerField(default=0)
    sell_rate = models.IntegerField(default=0)
    # --------------------------------- showcase information -----------------------------------
    size = models.CharField(max_length=80, blank=True, null=True)
    brand = models.CharField(max_length=80, blank=True, null=True)
    model = models.CharField(max_length=80, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    buy_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    sell_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    features = models.ManyToManyField(Feature, blank=True)

    def get_features(self):
        return "\n".join([p.en_title for p in self.features.all()])

    def __str__(self):
        return self.en_title


class Collection(models.Model):
    # --------------------------------- relation informations ----------------------------------
    en_title = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- relation types -----------------------------------------
    size = models.ManyToManyField(Product, blank=True)
    set = models.ManyToManyField(Product, blank=True)
    color = models.ManyToManyField(Product, blank=True)

    def sizes(self):
        return "\n".join([p.en_title for p in self.size.all()])

    def sets(self):
        return "\n".join([p.en_title for p in self.set.all()])

    def colors(self):
        return "\n".join([p.en_title for p in self.color.all()])

    def __str__(self):
        return self.en_title
