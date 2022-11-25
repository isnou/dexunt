from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Feature(models.Model):
    # --------------------------------- feature types ------------------------------------------
    en_title = models.CharField(max_length=15, blank=True, null=True)
    fr_title = models.CharField(max_length=15, blank=True, null=True)
    ar_title = models.CharField(max_length=15, blank=True, null=True)
    # --------------------------------- feature value ------------------------------------------
    en_value = models.TextField(max_length=1000, null=True)
    fr_value = models.TextField(max_length=1000, null=True)
    ar_value = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return self.en_title


class Product(models.Model):
    # --------------------------------- product identification en ------------------------------
    en_product_title = models.CharField(max_length=200, blank=True, null=True)
    en_variant = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- product identification fr ------------------------------
    fr_product_title = models.CharField(max_length=200, blank=True, null=True)
    fr_variant = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- product identification ar ------------------------------
    ar_product_title = models.CharField(max_length=200, blank=True, null=True)
    ar_variant = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- media --------------------------------------------------
    thumb = models.ImageField(upload_to='shop-manager/product/thumb', blank=True, null=True)
    # --------------------------------- technical details --------------------------------------
    upc = models.CharField(max_length=20, unique=True, null=True)
    sku = models.CharField(max_length=20, unique=True, null=True)
    tag = models.CharField(max_length=500, blank=True, default='tag')
    review_rate = models.IntegerField(
        default=5,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )
    sell_rate = models.IntegerField(
        default=5,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )
    # --------------------------------- showcase information -----------------------------------
    type = models.CharField(max_length=80, blank=True, null=True)
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
        return self.en_product_title
