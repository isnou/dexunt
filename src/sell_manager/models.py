from django.db import models
from shop_manager.models import Product
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
    sku = models.CharField(max_length=30, blank=True, null=True)
    clips = models.ManyToManyField(Clip, blank=True)
    # --------------------------------- media --------------------------------------------------
    thumb = models.ImageField(upload_to='sell-manager/collection/thumb', blank=True, null=True)
    # --------------------------------- info ---------------------------------------------------
    product_name = models.CharField(max_length=300, blank=True, null=True)
    product_option = models.CharField(max_length=300, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product_name
