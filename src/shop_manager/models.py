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
    image = models.ImageField(upload_to='shop-manager/product/')

    class Meta:
        verbose_name_plural = "Album"

    def __str__(self):
        return self.file_name


class Size(models.Model):
    # --------------------------------- product identification ---------------------------------
    en_title = models.CharField(max_length=200, blank=True, null=True)
    fr_title = models.CharField(max_length=200, blank=True, null=True)
    ar_title = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- media --------------------------------------------------
    thumb = models.ImageField(upload_to='shop-manager/size/', blank=True, null=True)
    # --------------------------------- technical details --------------------------------------
    show_thumb = models.BooleanField(default=False)
    upc = models.CharField(max_length=20, unique=True, null=True)
    sku = models.CharField(max_length=20, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sell_rate = models.IntegerField(default=0)
    # --------------------------------- showcase information -----------------------------------
    quantity = models.IntegerField(default=0)
    buy_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    sell_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.en_title


class Product(models.Model):
    # --------------------------------- product identification ---------------------------------
    en_title = models.CharField(max_length=200, blank=True, null=True)
    fr_title = models.CharField(max_length=200, blank=True, null=True)
    ar_title = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- product specs ------------------------------------------
    en_spec = models.CharField(max_length=200, blank=True, null=True)
    fr_spec = models.CharField(max_length=200, blank=True, null=True)
    ar_spec = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- media --------------------------------------------------
    album = models.ManyToManyField(Album, blank=True)
    # --------------------------------- technical details --------------------------------------
    publish = models.BooleanField(default=True)
    upc = models.CharField(max_length=20, unique=True, null=True)
    sku = models.CharField(max_length=20, unique=True, null=True)
    tag = models.CharField(max_length=500, blank=True, default='tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    review_rate = models.IntegerField(default=0)
    sell_rate = models.IntegerField(default=0)
    # --------------------------------- showcase information -----------------------------------
    size = models.ManyToManyField(Size, blank=True)
    quantity = models.IntegerField(default=0)
    buy_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    sell_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    feature = models.ManyToManyField(Feature, blank=True)

    def features(self):
        return "\n".join([p.en_title for p in self.feature.all()])

    def sizes(self):
        return "\n".join([p.value for p in self.size.all()])

    def __str__(self):
        return self.en_title


class ShowcaseProduct(models.Model):
    # --------------------------------- product identification ---------------------------------
    en_title = models.CharField(max_length=200, blank=True, null=True)
    fr_title = models.CharField(max_length=200, blank=True, null=True)
    ar_title = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- media --------------------------------------------------
    thumb = models.ImageField(upload_to='shop-manager/showcase/', blank=True, null=True)
    # --------------------------------- technical details --------------------------------------
    publish = models.BooleanField(default=True)
    availability = models.CharField(max_length=80, blank=True, null=True)
    sku = models.CharField(max_length=20, unique=True, null=True)
    tag = models.CharField(max_length=500, blank=True, default='tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    review_rate = models.IntegerField(default=0)
    sell_rate = models.IntegerField(default=0)
    # --------------------------------- showcase information -----------------------------------
    product = models.ManyToManyField(Product, blank=True)
    brand = models.CharField(max_length=80, blank=True, null=True)
    model = models.CharField(max_length=80, blank=True, null=True)
    sell_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def products(self):
        return "\n".join([p.en_title for p in self.product.all()])

    def __str__(self):
        return self.en_title
