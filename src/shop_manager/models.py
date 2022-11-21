from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Album(models.Model):
    # --------------------------------- picture types ------------------------------------------
    file_name = models.CharField(max_length=500, blank=True, default='product-image')
    # --------------------------------- picture location ---------------------------------------
    picture = models.ImageField(upload_to='shop-manager/product/album')

    def __str__(self):
        return self.file_name


class Feature(models.Model):
    # --------------------------------- feature types ------------------------------------------
    type = models.CharField(max_length=15, blank=True, null=True)
    # --------------------------------- feature language ---------------------------------------
    language = models.CharField(max_length=15, blank=True, default='english')
    # --------------------------------- feature value ------------------------------------------
    value = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return self.value


class Product(models.Model):
    # --------------------------------- product identification en ------------------------------
    en_product_name = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- product identification fr ------------------------------
    fr_product_name = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- product identification ar ------------------------------
    ar_product_name = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- additional option --------------------------------------
    option = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- media --------------------------------------------------
    thumb = models.ImageField(upload_to='shop-manager/product/thumb', blank=True, null=True)
    album = models.ManyToManyField(Album, blank=True)
    # --------------------------------- technical details --------------------------------------
    sku = models.CharField(max_length=20, unique=True, null=True)
    upc = models.CharField(max_length=20, unique=True, null=True)
    quantity = models.IntegerField(default=0)
    buy_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    rate = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )
    profile = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )

    def get_album(self):
        return "\n".join([p.file_name for p in self.album.all()])

    def __str__(self):
        return self.en_product_name


class Collection(models.Model):
    # --------------------------------- product identification en ------------------------------
    en_product_name = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- product identification fr ------------------------------
    fr_product_name = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- product identification ar ------------------------------
    ar_product_name = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- media --------------------------------------------------
    thumb = models.ImageField(upload_to='shop-manager/product/thumb', blank=True, null=True)
    # --------------------------------- technical details --------------------------------------
    brand = models.CharField(max_length=200, blank=True, null=True)
    model = models.CharField(max_length=200, blank=True, null=True)
    sku = models.CharField(max_length=20, unique=True, null=True)
    products = models.ManyToManyField(Product, blank=True)
    tag = models.CharField(max_length=500, blank=True, default='tag')
    rate = models.IntegerField(
        default=5,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )
    profile = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )
    # --------------------------------- showcase information -----------------------------------
    sel_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    features = models.ManyToManyField(Feature, blank=True)

    def get_products(self):
        return "\n".join([p.product_name for p in self.products.all()])

    def get_features(self):
        return "\n".join([p.value for p in self.features.all()])

    def __str__(self):
        return self.en_product_name
