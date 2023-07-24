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
    product_token = models.CharField(max_length=24, null=True)
    provider_token = models.CharField(max_length=24, null=True)
    # ----- #
    sale = models.IntegerField(default=0)
    delivery_quotient = models.IntegerField(default=100)
    points = models.IntegerField(default=0)
    max_quantity = models.IntegerField(default=0)
    tags = models.CharField(max_length=800, blank=True, null=True)
    # ----- relations ----- #
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
        if self.product_token:
            selected_product = Product.objects.all().get(token=self.product_token)
            for v in selected_product.variant.all():
                for o in v.option.all():
                    if self.upc == o.upc:
                        v.price = self.price
                        v.discount = self.discount
                        v.save()
        super().save()
    def duplicate(self, selected_variant):
        new_option = Option(product_token = self.product_token,
                            provider_token = self.provider_token,
                            delivery_quotient = self.delivery_quotient,
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
        selected_variant.option.add(new_option)
    def get_product(self):
        return Product.objects.all().get(token=self.product_token)
# ---------------------------------------------------------------------- #

# ------------------------------- Regular ------------------------------ #
class Variant(models.Model):
    # ----- Technical ----- #
    is_activated = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)
    # ----- #
    product_token = models.CharField(max_length=24, null=True)
    provider_token = models.CharField(max_length=24, null=True)
    # ----- #
    like = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)
    sale = models.IntegerField(default=0)
    created_at = models.DateTimeField(blank=True, null=True)
    tags = models.CharField(max_length=9000, blank=True, null=True)
    # ----- relations ----- #
    album = models.ManyToManyField(Album, blank=True)
    option = models.ManyToManyField(Option, blank=True)
    feature = models.ManyToManyField(Feature, blank=True)
    description = models.ManyToManyField(Description, blank=True)
    # ----- content ----- #
    en_title = models.CharField(max_length=200, blank=True, null=True)
    fr_title = models.CharField(max_length=200, blank=True, null=True)
    ar_title = models.CharField(max_length=200, blank=True, null=True)
    # ----- #
    en_spec = models.CharField(max_length=200, blank=True, null=True)
    fr_spec = models.CharField(max_length=200, blank=True, null=True)
    ar_spec = models.CharField(max_length=200, blank=True, null=True)
    # ----- #
    brand = models.CharField(max_length=80, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    # ----- functions ----- #
    def save(self, *args, **kwargs):
        if self.discount:
            if self.price < self.discount:
                self.discount = None
        super().save()
    def set_option(self, new_option):
        new_option.product_token = self.product_token
        new_option.save()
        self.price = new_option.price
        self.discount = new_option.discount
        self.option.add(new_option)
        super().save()
    def set_standard_features(self):
        new_feature = Feature(en_name = 'weight',
                              fr_name = 'poids',
                              ar_name = 'الوزن',
                              en_content = 'gr',
                              fr_content = 'gr',
                              ar_content = 'غرام',
                              )
        new_feature.save()
        self.feature.add(new_feature)

        new_feature = Feature(en_name='length',
                              fr_name='longueur',
                              ar_name='طول',
                              en_content='mm',
                              fr_content='mm',
                              ar_content='ملم',
                              )
        new_feature.save()
        self.feature.add(new_feature)

        new_feature = Feature(en_name='width',
                              fr_name='largeur',
                              ar_name='عرض',
                              en_content='mm',
                              fr_content='mm',
                              ar_content='ملم',
                              )
        new_feature.save()
        self.feature.add(new_feature)

        new_feature = Feature(en_name='height',
                              fr_name='hauteur',
                              ar_name='ارتفاع',
                              en_content='mm',
                              fr_content='mm',
                              ar_content='ملم',
                              )
        new_feature.save()
        self.feature.add(new_feature)

        new_feature = Feature(en_name='diameter',
                              fr_name='diamètre',
                              ar_name='القطر',
                              en_content='mm',
                              fr_content='mm',
                              ar_content='ملم',
                              )
        new_feature.save()
        self.feature.add(new_feature)

        new_feature = Feature(en_name='material',
                              fr_name='matière',
                              ar_name='مادة الصنع',
                              en_content='',
                              fr_content='',
                              ar_content='',
                              )
        new_feature.save()
        self.feature.add(new_feature)
    def get_product(self):
        return Product.objects.all().get(token=self.product_token)
    def clean(self):
        quantity = 0
        for option in self.option.all():
            if option.is_activated:
                quantity += option.quantity
        if quantity:
            self.is_available = True
        else:
            self.is_available = False
        super().save()
    def reset(self):
        self.created_at = timezone.now()
        super().save()
    def set_tags(self):
        self.tags = ''
        if self.en_title:
            self.tags += ('' + self.en_title)
        if self.en_title:
            self.tags += (', ' + self.en_title)
        if self.en_title:
            self.tags += (', ' + self.en_title)
        if self.option.all().count():
            for o in self.option.all():
                self.tags += (', ' + o.tags)
        if self.feature.all().count():
            for f in self.feature.all():
                self.tags += (', ' + f.tags)
        super().save()
    def duplicate(self):
        selected_product = Product.objects.all().get(token=self.product_token)
        new_variant = Variant(product_token = self.product_token,
                              provider_token = self.provider_token,
                              en_title = self.en_title,
                              fr_title = self.fr_title,
                              ar_title = self.ar_title,
                              en_spec = self.en_spec,
                              fr_spec = self.fr_spec,
                              ar_spec = self.ar_spec,
                              brand = self.brand,
                              price=self.price,
                              discount=self.discount
                              )
        new_variant.save()
        if self.option.all().count:
            for o in self.option.all():
                o.upc = None
                o.pk = None
                o.save()
                new_variant.option.add(o)
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
        selected_product.variant.add(new_variant)
    def activate(self):
        deactivate = True
        for option in self.option.all():
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
    # ----- Technical ----- #
    token = models.CharField(max_length=24, unique=True, null=True)
    provider_token = models.CharField(max_length=24, null=True)
    # ----- relations ----- #
    variant = models.ManyToManyField(Variant, blank=True)
    # ----- content ----- #
    en_title = models.CharField(max_length=200, blank=True, null=True)
    fr_title = models.CharField(max_length=200, blank=True, null=True)
    ar_title = models.CharField(max_length=200, blank=True, null=True)
    # ----- #
    brand = models.CharField(max_length=80, blank=True, null=True)
    # ----- functions ----- #
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = functions.serial_number_generator(24).upper()
        super().save()
    def update(self):
        for v in self.variant.all():
            v.provider_token = self.provider_token
            v.product_token = self.token
            v.en_title = self.en_title
            v.fr_title = self.fr_title
            v.ar_title = self.ar_title
            v.set_tags()
            v.save()
        super().save()
    def set_variant(self, new_variant):
        new_variant.product_token = self.token
        new_variant.en_title = self.en_title
        new_variant.fr_title = self.fr_title
        new_variant.ar_title = self.ar_title
        new_variant.save()
        self.variant.add(new_variant)
    def set_provider(self, store_name):
        selected_store = Store.objects.all().get(name=store_name)
        self.provider_token = selected_store.user.token
        self.brand = store_name
        for v in self.variant.all():
            v.provider_token = selected_store.user.token
            v.brand = store_name
            if v.option.all().count():
                for o in v.option.all():
                    o.provider_token = selected_store.user.token
            v.set_tags()
        super().save()
        selected_store.product.add(self)
    def unset_provider(self):
        store_name = self.brand
        self.provider_token = None
        self.brand = None
        for v in self.variant.all():
            v.provider_token = None
            v.brand = None
            if v.option.all().count():
                for o in v.option.all():
                    o.provider_token = None
            v.set_tags()
        super().save()
        if Store.objects.all().filter(name=self.store_name).exists():
            selected_store = Store.objects.all().get(name=self.store_name)
            selected_store.product.remove(self)
# ---------------------------------------------------------------------- #

# -------------------------- Special Products -------------------------- #
class Store(models.Model):
    # ----- Technical ----- #
    token = models.CharField(max_length=20, unique=True, null=True)
    tags = models.CharField(max_length=5000, blank=True, null=True)
    # ----- relations ----- #
    product = models.ManyToManyField(Product, blank=True)
    # ----- content ----- #
    name = models.CharField(max_length=200, unique=True, null=True)
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

        if not self.token:
            self.token = functions.serial_number_generator(20).upper()

        super().save()
#                                                                        #
class FlashProduct(models.Model):
    # ----- Technical ----- #
    upc = models.CharField(max_length=20, blank=True, null=True)
    product_token = models.CharField(max_length=24, null=True)
    valid_until = models.DateTimeField(blank=True, null=True)
    is_activated = models.BooleanField(default=False)
    # ----- relations ----- #
    # ----- media ----- #
    def get_image_path(self, filename):
        return self.en_title.lower()
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    # ----- content ----- #
    en_title = models.CharField(max_length=200, blank=True, null=True)
    fr_title = models.CharField(max_length=200, blank=True, null=True)
    ar_title = models.CharField(max_length=200, blank=True, null=True)
    # ----- #
    en_spec = models.CharField(max_length=200, blank=True, null=True)
    fr_spec = models.CharField(max_length=200, blank=True, null=True)
    ar_spec = models.CharField(max_length=200, blank=True, null=True)
    # ----- #
    en_value = models.CharField(max_length=200, blank=True, null=True)
    fr_value = models.CharField(max_length=200, blank=True, null=True)
    ar_value = models.CharField(max_length=200, blank=True, null=True)
    # ----- #
    quantity = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    # ----- functions ----- #
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
# ---------------------------------------------------------------------- #


# ------------------------------- Title -------------------------------- #
# ----- Technical ----- #
# ----- relations ----- #
# ----- media ----- #
# ----- content ----- #
# ----- #
# ----- #
# ----- functions ----- #
# ---------------------------------------------------------------------- #