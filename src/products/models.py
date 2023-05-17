from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from add_ons import functions


class Feature(models.Model):
    # --------------------------------- feature title ------------------------------------------
    en_title = models.CharField(max_length=100, blank=True, null=True)
    fr_title = models.CharField(max_length=100, blank=True, null=True)
    ar_title = models.CharField(max_length=100, blank=True, null=True)
    # --------------------------------- feature value ------------------------------------------
    en_value = models.TextField(max_length=500, null=True)
    fr_value = models.TextField(max_length=500, null=True)
    ar_value = models.TextField(max_length=500, null=True)

    def __str__(self):
        return self.en_title

class Review(models.Model):
    # --------------------------------- feature types ------------------------------------------
    client_name = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=500, blank=True, null=True)
    rates = models.IntegerField(default=0)
    # --------------------------------- technical details --------------------------------------
    show = models.BooleanField(default=True)
    user_token = models.CharField(max_length=24, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client_name

class Album(models.Model):
    file_name = models.CharField(max_length=500, blank=True)
    def get_image_path(self, filename):
        return self.file_name.lower()
    image = models.ImageField(upload_to=get_image_path)

    class Meta:
        verbose_name_plural = "Album"

    def __str__(self):
        return self.file_name

class Option(models.Model):
    # --------------------------------- product identification ---------------------------------
    en_value = models.CharField(max_length=200, blank=True, null=True)
    fr_value = models.CharField(max_length=200, blank=True, null=True)
    ar_value = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- media --------------------------------------------------
    def get_image_path(self, filename):
        return self.en_value.lower()
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    # --------------------------------- technical details --------------------------------------
    has_image = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=True)
    product_token = models.CharField(max_length=24, null=True)
    review = models.ManyToManyField(Review, blank=True)
    sale = models.IntegerField(default=0)
    upc = models.CharField(max_length=20, unique=True, null=True)
    tag = models.CharField(max_length=500, blank=True, default='tag')
    created_at = models.DateTimeField(auto_now_add=True)
    # --------------------------------- inventory information ----------------------------------
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    # --------------------------------- showcase information -----------------------------------
    delivery_quotient = models.IntegerField(default=100)
    points = models.IntegerField(default=0)
    max_quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def reviews(self):
        return "\n".join([p.client_name for p in self.review.all()])

    def __str__(self):
        return self.en_value

class Variant(models.Model):
    # --------------------------------- product specs ------------------------------------------
    en_spec = models.CharField(max_length=200, blank=True, null=True)
    fr_spec = models.CharField(max_length=200, blank=True, null=True)
    ar_spec = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- media --------------------------------------------------
    album = models.ManyToManyField(Album, blank=True)
    # --------------------------------- technical details --------------------------------------
    availability = models.BooleanField(default=False)
    product_token = models.CharField(max_length=24, null=True)
    user_token = models.CharField(max_length=24, null=True)
    like = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)
    sale = models.IntegerField(default=0)
    # --------------------------------- showcase information -----------------------------------
    option = models.ManyToManyField(Option, blank=True)
    feature = models.ManyToManyField(Feature, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)


    def features(self):
        return "\n".join([p.en_title for p in self.feature.all()])

    def options(self):
        return "\n".join([p.en_value for p in self.option.all()])

    def __str__(self):
        return self.en_spec

class Product(models.Model):
    # --------------------------------- product identification ---------------------------------
    en_title = models.CharField(max_length=200, blank=True, null=True)
    fr_title = models.CharField(max_length=200, blank=True, null=True)
    ar_title = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- media --------------------------------------------------
    def get_image_path(self, filename):
        return self.en_title.lower()
    selected_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    # --------------------------------- technical details --------------------------------------
    product_token = models.CharField(max_length=24, unique=True, null=True)
    like = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)
    sale = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    # --------------------------------- showcase information -----------------------------------
    variant = models.ManyToManyField(Variant, blank=True)
    brand = models.CharField(max_length=80, blank=True, null=True)
    en_description = models.CharField(max_length=800, blank=True, null=True)
    fr_description = models.CharField(max_length=800, blank=True, null=True)
    ar_description = models.CharField(max_length=800, blank=True, null=True)
    en_note = models.CharField(max_length=500, blank=True, null=True)
    fr_note = models.CharField(max_length=500, blank=True, null=True)
    ar_note = models.CharField(max_length=500, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def variants(self):
        return "\n".join([p.en_spec for p in self.variant.all()])

    def save(self, *args, **kwargs):
        self.product_token = functions.serial_number_generator(24)
        super().save()

    def __str__(self):
        return self.en_title