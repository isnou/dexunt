from django.db import models
from shop_manager.models import Product
from django.core.validators import MaxValueValidator, MinValueValidator


class Clip(models.Model):
    # --------------------------------- clip technical informations ----------------------------
    sku = models.CharField(max_length=30, unique=True, null=True)
    product_title = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    # --------------------------------- clip info  ---------------------------------------------
    en_clip_title = models.CharField(max_length=100, blank=True, null=True)
    fr_clip_title = models.CharField(max_length=100, blank=True, null=True)
    ar_clip_title = models.CharField(max_length=100, blank=True, null=True)

    en_clip_detail = models.CharField(max_length=100, blank=True, null=True)
    fr_clip_detail = models.CharField(max_length=100, blank=True, null=True)
    ar_clip_detail = models.CharField(max_length=100, blank=True, null=True)

    value = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.product_title
