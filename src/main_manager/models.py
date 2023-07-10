from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from add_ons import functions

# --------------------- detail --------------------- #
class Review(models.Model):
    # --------------------------------- feature types ------------------------------------------
    client_name = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=500, blank=True, null=True)
    rates = models.IntegerField(default=0)
    # --------------------------------- technical details --------------------------------------
    show = models.BooleanField(default=True)
    user_token = models.CharField(max_length=24, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Album(models.Model):
    file_name = models.CharField(max_length=500, blank=True)
    def get_image_path(self, filename):
        return self.file_name.lower()
    image = models.ImageField(upload_to=get_image_path)

    class Meta:
        verbose_name_plural = "Album"

class Feature(models.Model):
    # --------------------------------- feature title ------------------------------------------
    en_name = models.CharField(max_length=100, blank=True, null=True)
    fr_name = models.CharField(max_length=100, blank=True, null=True)
    ar_name = models.CharField(max_length=100, blank=True, null=True)
    # --------------------------------- feature value ------------------------------------------
    en_content = models.TextField(max_length=500, null=True)
    fr_content = models.TextField(max_length=500, null=True)
    ar_content = models.TextField(max_length=500, null=True)

class Description(models.Model):
    # --------------------------------- feature title ------------------------------------------
    en_title = models.CharField(max_length=100, blank=True, null=True)
    fr_title = models.CharField(max_length=100, blank=True, null=True)
    ar_title = models.CharField(max_length=100, blank=True, null=True)
    # --------------------------------- feature value ------------------------------------------
    en_content = models.TextField(max_length=500, null=True)
    fr_content = models.TextField(max_length=500, null=True)
    ar_content = models.TextField(max_length=500, null=True)
    # --------------------------------- media --------------------------------------------------
    file_name = models.CharField(max_length=500, blank=True)
    def get_image_path(self, filename):
        return self.file_name.lower()

# ---------------- regular showcase ---------------- #
class Option(models.Model):
    # --------------------------------- product identification ---------------------------------
    en_value = models.CharField(max_length=200, blank=True, null=True)
    fr_value = models.CharField(max_length=200, blank=True, null=True)
    ar_value = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- media --------------------------------------------------
    file_name = models.CharField(max_length=500, blank=True)
    def get_image_path(self, filename):
        return self.file_name.lower()
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    # --------------------------------- technical details --------------------------------------
    has_image = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)
    product_token = models.CharField(max_length=24, null=True)
    review = models.ManyToManyField(Review, blank=True)
    sale = models.IntegerField(default=0)
    upc = models.CharField(max_length=20, unique=True, null=True)
    tag = models.CharField(max_length=500, blank=True, default='tag')
    # --------------------------------- inventory information ----------------------------------
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    # --------------------------------- showcase information -----------------------------------
    delivery_quotient = models.IntegerField(default=100)
    points = models.IntegerField(default=0)
    max_quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.upc:
            self.upc = functions.serial_number_generator(20).upper()
        if self.cost:
            if self.price < self.cost:
                self.cost = None
        if self.discount:
            if self.price < self.discount:
                self.discount = None
        super().save()

class Variant(models.Model):
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
    is_activated = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)
    product_token = models.CharField(max_length=24, null=True)
    user_token = models.CharField(max_length=24, null=True)
    like = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)
    sale = models.IntegerField(default=0)
    created_at = models.DateTimeField(blank=True, null=True)
    # --------------------------------- showcase information -----------------------------------
    brand = models.CharField(max_length=80, blank=True, null=True)
    option = models.ManyToManyField(Option, blank=True)
    feature = models.ManyToManyField(Feature, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.discount:
            if self.price < self.discount:
                self.discount = None
        super().save()

    def clean(self):
        quantity = 0
        for option in self.option.all():
            if option.is_activated:
                quantity += option.quantity
        if quantity:
            self.is_available = True
        else:
            self.is_available = False

        deactivate = True
        for option in self.option.all():
            if option.is_activated:
                deactivate = False
        if deactivate:
            self.is_activated = False
        super().save()

    def reset(self):
        self.created_at = timezone.now()
        super().save()

class Product(models.Model):
    # --------------------------------- product identification ---------------------------------
    en_title = models.CharField(max_length=200, blank=True, null=True)
    fr_title = models.CharField(max_length=200, blank=True, null=True)
    ar_title = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- technical details --------------------------------------
    product_token = models.CharField(max_length=24, unique=True, null=True)
    # --------------------------------- showcase information -----------------------------------
    brand = models.CharField(max_length=80, blank=True, null=True)
    variant = models.ManyToManyField(Variant, blank=True)
    description = models.ManyToManyField(Description, blank=True)
    en_note = models.CharField(max_length=500, blank=True, null=True)
    fr_note = models.CharField(max_length=500, blank=True, null=True)
    ar_note = models.CharField(max_length=500, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.product_token:
            self.product_token = functions.serial_number_generator(24).upper()
        super().save()

# ----------------- flash showcase ---------------- #
class FlashProduct(models.Model):
    # --------------------------------- product identification ---------------------------------
    en_title = models.CharField(max_length=200, blank=True, null=True)
    fr_title = models.CharField(max_length=200, blank=True, null=True)
    ar_title = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- product specs ------------------------------------------
    en_spec = models.CharField(max_length=200, blank=True, null=True)
    fr_spec = models.CharField(max_length=200, blank=True, null=True)
    ar_spec = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- product option -----------------------------------------
    en_value = models.CharField(max_length=200, blank=True, null=True)
    fr_value = models.CharField(max_length=200, blank=True, null=True)
    ar_value = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- media --------------------------------------------------
    def get_image_path(self, filename):
        return self.en_title.lower()

    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    # --------------------------------- technical details --------------------------------------
    upc = models.CharField(max_length=20, blank=True, null=True)
    product_token = models.CharField(max_length=24, null=True)
    valid_until = models.DateTimeField(blank=True, null=True)
    is_activated = models.BooleanField(default=False)
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    # --------------------------------- showcase information -----------------------------------
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.discount:
            if self.price < self.discount:
                self.discount = None
        super().save()

    def clean(self):
        if self.valid_until <= timezone.now():
            self.is_activated = False
        if self.quantity == 0:
            self.is_activated = False
        if not self.discount:
            self.is_activated = False
        super().save()


