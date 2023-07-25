from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from add_ons import functions
from PIL import Image

# ---------------------------- Requirements ---------------------------- #
class Review(models.Model):
    # ----- Technical ----- #
    show = models.BooleanField(default=True)
    user_token = models.CharField(max_length=24, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # ----- content ----- #
    client_name = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=500, blank=True, null=True)
    rates = models.IntegerField(default=0)
#                                                                        #
class Album(models.Model):
    # ----- media ----- #
    file_name = models.CharField(max_length=500, blank=True)
    def get_image_path(self, filename):
        return self.file_name.lower()
    image = models.ImageField(upload_to=get_image_path)
    # ----- relations ----- #
    variant = models.ForeignKey(
        'management.Variant', on_delete=models.CASCADE, null=True)
    # ----- functions ----- #
    class Meta:
        verbose_name_plural = "Album"
#                                                                        #
class Feature(models.Model):
    # ----- Technical ----- #
    tags = models.CharField(max_length=2000, blank=True, null=True)
    # ----- content ----- #
    en_name = models.CharField(max_length=100, blank=True, null=True)
    fr_name = models.CharField(max_length=100, blank=True, null=True)
    ar_name = models.CharField(max_length=100, blank=True, null=True)
    # ----- #
    en_content = models.TextField(max_length=500, null=True)
    fr_content = models.TextField(max_length=500, null=True)
    ar_content = models.TextField(max_length=500, null=True)
    def save(self):
        self.tags = ''
        if self.en_name:
            self.tags += (', ' + self.en_name)
        if self.fr_name:
            self.tags += (', ' + self.fr_name)
        if self.ar_name:
            self.tags += (', ' + self.ar_name)
        if self.en_content:
            self.tags += (', ' + self.en_content)
        if self.fr_content:
            self.tags += (', ' + self.fr_content)
        if self.ar_content:
            self.tags += (', ' + self.ar_content)
        super().save()
#                                                                        #
class Description(models.Model):
    # ----- Technical ----- #
    has_image = models.BooleanField(default=False)
    image_to_the_right = models.BooleanField(default=False)
    # ----- content ----- #
    en_title = models.CharField(max_length=100, blank=True, null=True)
    fr_title = models.CharField(max_length=100, blank=True, null=True)
    ar_title = models.CharField(max_length=100, blank=True, null=True)
    # ----- #
    en_content = models.TextField(max_length=500, null=True)
    fr_content = models.TextField(max_length=500, null=True)
    ar_content = models.TextField(max_length=500, null=True)
    # ----- media ----- #
    file_name = models.CharField(max_length=500, blank=True)
    def get_image_path(self, filename):
        return self.file_name.lower()
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
# ---------------------------------------------------------------------- #

# ------------------------------ Inventory ----------------------------- #
class Option(models.Model):
    # ----- Technical ----- #
    has_image = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)
    # ----- #
    upc = models.CharField(max_length=20, unique=True, null=True)
    # ----- #
    sale = models.IntegerField(default=0)
    delivery_quotient = models.IntegerField(default=100)
    points = models.IntegerField(default=0)
    max_quantity = models.IntegerField(default=0)
    tags = models.CharField(max_length=800, blank=True, null=True)
    # ----- relations ----- #
    variant = models.ForeignKey(
        'management.Variant', on_delete=models.CASCADE, null=True)
    review = models.ManyToManyField(Review, blank=True)
    # ----- media ----- #
    file_name = models.CharField(max_length=500, blank=True)
    def get_image_path(self, filename):
        return self.file_name.lower()
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    # ----- content ----- #
    en_value = models.CharField(max_length=200, blank=True, null=True)
    fr_value = models.CharField(max_length=200, blank=True, null=True)
    ar_value = models.CharField(max_length=200, blank=True, null=True)
    # ----- #
    en_note = models.CharField(max_length=500, blank=True, null=True)
    fr_note = models.CharField(max_length=500, blank=True, null=True)
    ar_note = models.CharField(max_length=500, blank=True, null=True)
    # ----- #
    quantity = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    # ----- functions ----- #
    def save(self, *args, **kwargs):
        if not self.upc:
            self.upc = functions.serial_number_generator(20).upper()
        if self.cost:
            if self.price < self.cost:
                self.cost = None
        if self.discount:
            if self.price < self.discount:
                self.discount = None
        self.tags = ''
        if self.en_value:
            self.tags += ('' + self.en_value)
        if self.fr_value:
            self.tags += (', ' + self.fr_value)
        if self.ar_value:
            self.tags += (', ' + self.ar_value)
        super().save()
    def duplicate(self):
        new_option = Option(delivery_quotient = self.delivery_quotient,
                            points = self.points,
                            max_quantity = self.max_quantity,
                            en_value = self.en_value,
                            fr_value = self.fr_value,
                            ar_value = self.ar_value,
                            en_note = self.en_note,
                            fr_note = self.fr_note,
                            ar_note = self.ar_note,
                            cost = self.cost,
                            price = self.price,
                            discount = self.discount
                            )
        new_option.save()
        self.variant.option_set.add(new_option)
# ---------------------------------------------------------------------- #

# ------------------------------- Regular ------------------------------ #
class Variant(models.Model):
    # ----- Technical ----- #
    is_activated = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)
    # ----- #
    like = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)
    sale = models.IntegerField(default=0)
    created_at = models.DateTimeField(blank=True, null=True)
    tags = models.CharField(max_length=9000, blank=True, null=True)
    # ----- relations ----- #
    # related to many options #
    # related to many albums #
    feature = models.ManyToManyField(Feature, blank=True)
    description = models.ManyToManyField(Description, blank=True)
    product = models.ForeignKey(
        'management.Product', on_delete=models.CASCADE, null=True)
    # ----- content ----- #
    en_spec = models.CharField(max_length=200, blank=True, null=True)
    fr_spec = models.CharField(max_length=200, blank=True, null=True)
    ar_spec = models.CharField(max_length=200, blank=True, null=True)
    # ----- functions ----- #
    def clean(self):
        quantity = 0
        for option in self.option_set.all():
            if option.is_activated:
                quantity += option.quantity
        if quantity:
            self.is_available = True
        else:
            self.is_available = False
        super().save()
    def set_tags(self):
        self.tags = ''
        if self.product.en_title:
            self.tags += ('' + self.product.en_title)
        if self.product.fr_title:
            self.tags += (', ' + self.product.fr_title)
        if self.product.ar_title:
            self.tags += (', ' + self.product.ar_title)

        if self.en_spec:
            self.tags += (', ' + self.en_spec)
        if self.fr_spec:
            self.tags += (', ' + self.fr_spec)
        if self.ar_spec:
            self.tags += (', ' + self.ar_spec)

        if self.option_set.all().count():
            for o in self.option_set.all():
                self.tags += (', ' + o.tags)
        if self.feature.all().count():
            for f in self.feature.all():
                self.tags += (', ' + f.tags)

        super().save()
    def duplicate(self):
        new_variant = Variant(en_spec = self.en_spec,
                              fr_spec = self.fr_spec,
                              ar_spec = self.ar_spec,
                              )
        new_variant.save()
        if self.option_set.all().count:
            for o in self.option_set.all():
                o.upc = None
                o.pk = None
                o.save()
                new_variant.option_set.add(o)
        if self.feature.all().count:
            for f in self.feature.all():
                f.pk = None
                f.save()
                new_variant.feature.add(f)
        if self.description.all().count:
            for d in self.description.all():
                d.pk = None
                d.save()
                new_variant.description.add(d)
        self.product.variant_set.add(new_variant)
    def activate(self):
        deactivate = True
        for option in self.option_set.all():
            if option.is_activated:
                deactivate = False
        if not deactivate:
            self.is_activated = True
        super().save()
    def deactivate(self):
        self.is_activated = False
        super().save()
#                                                                        #
class Product(models.Model):
    # ----- relations ----- #
    # related to many variants #
    store = models.ForeignKey(
        'management.Store', on_delete=models.CASCADE, null=True)
    # ----- content ----- #
    en_title = models.CharField(max_length=200, blank=True, null=True)
    fr_title = models.CharField(max_length=200, blank=True, null=True)
    ar_title = models.CharField(max_length=200, blank=True, null=True)
    # ----- #
    brand = models.CharField(max_length=80, blank=True, null=True)
    # ----- functions ----- #
    def update_tags(self):
        for v in self.variant_set.all():
            v.set_tags()
            v.save()
# ---------------------------------------------------------------------- #

# -------------------------- Special Products -------------------------- #
class Store(models.Model):
    # ----- Technical ----- #
    tags = models.CharField(max_length=5000, blank=True, null=True)
    is_activated = models.BooleanField(default=False)
    # ----- content ----- #
    name = models.CharField(max_length=200, unique=True, null=True)
    # ----- relations ----- #
    # related to many products #
    # ----- #
    en_activity = models.CharField(max_length=300, blank=True, null=True)
    fr_activity = models.CharField(max_length=300, blank=True, null=True)
    ar_activity = models.CharField(max_length=300, blank=True, null=True)
    # ----- #
    en_description = models.CharField(max_length=600, blank=True, null=True)
    fr_description = models.CharField(max_length=600, blank=True, null=True)
    ar_description = models.CharField(max_length=600, blank=True, null=True)
    # ----- #
    en_address = models.CharField(max_length=300, blank=True, null=True)
    fr_address = models.CharField(max_length=300, blank=True, null=True)
    ar_address = models.CharField(max_length=300, blank=True, null=True)
    # ----- functions ----- #
    def save(self, *args, **kwargs):
        self.tags = ''
        if self.name:
            self.tags += (', ' + self.name)

        if self.en_activity:
            self.tags += (', ' + self.en_activity)
        if self.fr_activity:
            self.tags += (', ' + self.fr_activity)
        if self.ar_activity:
            self.tags += (', ' + self.ar_activity)

        if self.en_description:
            self.tags += (', ' + self.en_description)
        if self.fr_description:
            self.tags += (', ' + self.fr_description)
        if self.ar_description:
            self.tags += (', ' + self.ar_description)

        if self.en_address:
            self.tags += (', ' + self.en_address)
        if self.fr_address:
            self.tags += (', ' + self.fr_address)
        if self.ar_address:
            self.tags += (', ' + self.ar_address)

        super().save()
    def activate(self):
        if self.user.profile_photo and self.name:
            self.is_activated = True
            super().save()
#                                                                        #
class FlashProduct(models.Model):
    # ----- Technical ----- #
    upc = models.CharField(max_length=20, blank=True, null=True)
    product_token = models.CharField(max_length=24, null=True)
    valid_until = models.DateTimeField(blank=True, null=True)
    is_activated = models.BooleanField(default=False)
    # ----- relations ----- #
    option = models.OneToOneField(
        Option,
        on_delete=models.CASCADE,
        null=True
    )
    # ----- content ----- #
    quantity = models.IntegerField(default=0)
    discount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    # ----- functions ----- #
    def clean(self):
        if self.valid_until <= timezone.now():
            self.is_activated = False
        if self.quantity == 0:
            self.is_activated = False
        if not self.discount:
            self.is_activated = False
        super().save()
# ---------------------------------------------------------------------- #
