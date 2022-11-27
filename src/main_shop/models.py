from django.db import models
from shop_manager.models import Product
from django.core.validators import MaxValueValidator, MinValueValidator


class Layout(models.Model):
    # --------------------------------- layout types -------------------------------------------
    type = models.CharField(max_length=25, blank=True, null=True)
    # --------------------------------- layout titles ------------------------------------------
    en_first_title = models.TextField(max_length=500, blank=True, null=True)
    en_second_title = models.TextField(max_length=500, blank=True, null=True)
    en_third_title = models.TextField(max_length=500, blank=True, null=True)

    fr_first_title = models.TextField(max_length=500, blank=True, null=True)
    fr_second_title = models.TextField(max_length=500, blank=True, null=True)
    fr_third_title = models.TextField(max_length=500, blank=True, null=True)

    ar_first_title = models.TextField(max_length=500, blank=True, null=True)
    ar_second_title = models.TextField(max_length=500, blank=True, null=True)
    ar_third_title = models.TextField(max_length=500, blank=True, null=True)
    # --------------------------------- buttons ------------------------------------------------
    en_button = models.TextField(max_length=40, blank=True, null=True)
    fr_button = models.TextField(max_length=40, blank=True, null=True)
    ar_button = models.TextField(max_length=40, blank=True, null=True)
    # --------------------------------- additional information ---------------------------------
    link = models.TextField(max_length=500, blank=True, null=True)
    thumb = models.ImageField(upload_to='main-shop/e-shop/thumb', blank=True, null=True)
    products = models.ManyToManyField(Product, blank=True)
    # --------------------------------- expiration ---------------------------------------------
    day = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    def get_products(self):
        return "\n".join([p.en_product_title for p in self.products.all()])

    def __str__(self):
        return self.type
