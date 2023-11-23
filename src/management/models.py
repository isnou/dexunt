from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from add_ons import functions
from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField


# ---------------------------- Requirements ---------------------------- #
class Review(models.Model):
    # ----- Technical ----- #
    show = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # ----- relations ----- #
    option = models.ForeignKey('management.Option', on_delete=models.CASCADE, related_name='reviews', null=True)
    client = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='reviews', null=True)
    # ----- content ----- #
    content = models.CharField(max_length=500, blank=True, null=True)
    rate = models.IntegerField(default=0)
    # ----- variables ----- #
    def star_one(self):
        if self.rate > 0:
            return '-fill'
        else:
            return ''
    def star_two(self):
        if self.rate > 1:
            return '-fill'
        else:
            return ''
    def star_three(self):
        if self.rate > 2:
            return '-fill'
        else:
            return ''
    def star_four(self):
        if self.rate > 3:
            return '-fill'
        else:
            return ''
    def star_five(self):
        if self.rate > 4:
            return '-fill'
        else:
            return ''
#                                                                        #
class Like(models.Model):
    # ----- Technical ----- #
    created_at = models.DateTimeField(auto_now_add=True)
    # ----- relations ----- #
    option = models.ForeignKey('management.Option', on_delete=models.CASCADE, related_name='likes', null=True)
    client = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='likes', null=True)
#                                                                        #
class Album(models.Model):
    # ----- media ----- #
    file_name = models.CharField(max_length=500, blank=True)
    def get_image_path(self, filename):
        return self.file_name.lower()
    image = models.ImageField(upload_to=get_image_path)
    # ----- relations ----- #
    variant = models.ForeignKey('management.Variant', on_delete=models.CASCADE, null=True)
    # ----- functions ----- #
    class Meta:
        verbose_name_plural = "Album"
#                                                                        #
class Feature(models.Model):
    # ----- relations ----- #
    variant = models.ForeignKey('management.Variant', on_delete=models.CASCADE, null=True)
    # ----- content ----- #
    en_name = models.CharField(max_length=100, blank=True, null=True)
    fr_name = models.CharField(max_length=100, blank=True, null=True)
    ar_name = models.CharField(max_length=100, blank=True, null=True)
    # ----- #
    en_content = models.TextField(max_length=500, null=True)
    fr_content = models.TextField(max_length=500, null=True)
    ar_content = models.TextField(max_length=500, null=True)
    # ----- functions ----- #
    def name(self):
        language = global_request.session.get('language')
        if language == 'en-us':
            return self.en_name
        if language == 'fr-fr':
            return self.fr_name
        if language == 'ar-dz':
            return self.ar_name
    def content(self):
        language = global_request.session.get('language')
        if language == 'en-us':
            return self.en_content
        if language == 'fr-fr':
            return self.fr_content
        if language == 'ar-dz':
            return self.ar_content
# ---------------------------------------------------------------------- #

# ------------------------------ Inventory ----------------------------- #
class Option(models.Model):
    # ----- Technical ----- #
    has_image = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)
    out_of_stock = models.BooleanField(default=False)
    # ----- #
    upc = models.CharField(max_length=20, unique=True, null=True)
    # ----- relations ----- #
    variant = models.ForeignKey('management.Variant', on_delete=models.CASCADE, null=True)
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
    restricted_quantity = models.IntegerField(default=0)
    production_capacity_quantity = models.IntegerField(default=0)
    production_capacity_time = models.DurationField(blank=True, null=True)
    delivery_quotient = models.IntegerField(default=100)
    points = models.IntegerField(default=0)
    # ----- #
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    min_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    # ----- functions ----- #
    def save(self, *args, **kwargs):
        if not self.upc:
            self.upc = functions.serial_number_generator(20).upper()
        if self.limited_stock():
            if self.production_capacity_quantity:
                self.out_of_stock = False
            else:
                self.out_of_stock = True
        super().save()
    def duplicate(self):
        new_option = Option(delivery_quotient = self.delivery_quotient,
                            points = self.points,
                            restricted_quantity = self.restricted_quantity,
                            en_note = self.en_note,
                            fr_note = self.fr_note,
                            ar_note = self.ar_note,
                            cost = self.cost,
                            price = self.price,
                            min_price = self.min_price,
                            discount = self.discount
                            )
        new_option.save()
        self.variant.option_set.add(new_option)
    def add_production_capacity(self, request):
        self.production_capacity_quantity = int(request.POST.get('quantity', False))
        duration = request.POST.get('duration', False)
        if duration == 'one_day':
            self.production_capacity_time = timedelta(hours=24)
            self.deactivate()
        if duration == 'one_month':
            self.production_capacity_time = timedelta(weeks=4)
            self.deactivate()
        if duration == 'limited_stock':
            self.production_capacity_time = timedelta(days=365)
        self.save()
    def activate(self):
        if self.product_ready():
            self.is_activated = True
            self.save()
            self.variant.activate()
    def deactivate(self):
        self.is_activated = False
        self.save()
        self.variant.activate()
    def add_a_review(self, request):
        comment = request.POST.get('comment', False)
        rating = request.POST.get('rating', False)
        Review(content=comment,
               rate=rating,
               option=self,
               client=request.user
               ).save()
    def refund_request(self, request):
        comment = request.POST.get('comment', False)
        Review(content=comment,
               show=False,
               option=self,
               client=request.user
               ).save()
    def start_production(self):
        self.out_of_stock = False
        super().save()
    def stop_production(self):
        self.out_of_stock = True
        super().save()
    # ----- variables ----- #
    def store_ready(self):
        if self.production_capacity_time and self.cost:
            if self.production_capacity_quantity or self.limited_stock():
                return True
            else:
                return False
        else:
            return False
    def product_ready(self):
        if self.store_ready() and self.price:
            return True
        else:
            return False
    def limited_stock(self):
        if self.production_capacity_time:
            if self.production_capacity_time == timedelta(days=365):
                return True
            else:
                return False
        else:
            return False
    def can_be_activated(self):
        if self.variant.product.store:
            return self.variant.product.store.is_activated
        else:
            return False
    def value(self):
        language = global_request.session.get('language')
        if language == 'en-us':
            return self.en_value
        if language == 'fr-fr':
            return self.fr_value
        if language == 'ar-dz':
            return self.ar_value
    def note(self):
        language = global_request.session.get('language')
        if language == 'en-us':
            return self.en_note
        if language == 'fr-fr':
            return self.fr_note
        if language == 'ar-dz':
            return self.ar_note
    def discount_percentage(self):
        if self.discount:
            if int(( 100 * (self.price - self.discount)) / self.price) >= 10:
                return int(( 100 * (self.price - self.discount)) / self.price)
            else:
                return False
        else:
            return False
    def likes(self):
        like = 0
        for l in self.likes.all():
            like += 1
        return like
    def rates(self):
        rate = 0
        for r in self.reviews.all().filter(show=True):
            rate += r.rate
        if self.reviews.all().filter(show=True).count():
            return rate/self.reviews.all().filter(show=True).count()
        else:
            return 0
    def sales(self):
        sale = 0
        for s in self.selected_products.all().filter(status='completed'):
            sale += 1
        return sale
    def refunds(self):
        refund = 0
        for s in self.selected_products.all().filter(status='refunded'):
            refund += 1
        return refund
    def rate_by_sales(self):
        return self.rates() * self.sales()
    def review_star_one(self):
        if self.rates() == 0:
            return ''
        if self.rates() > 0:
            if self.rates() < 1:
                return '-half'
            else:
                return '-fill'
    def review_star_two(self):
        if self.rates() <= 1:
            return ''
        if self.rates() > 1:
            if self.rates() < 2:
                return '-half'
            else:
                return '-fill'
    def review_star_three(self):
        if self.rates() <= 2:
            return ''
        if self.rates() > 2:
            if self.rates() < 3:
                return '-half'
            else:
                return '-fill'
    def review_star_four(self):
        if self.rates() <= 3:
            return ''
        if self.rates() > 3:
            if self.rates() < 4:
                return '-half'
            else:
                return '-fill'
    def review_star_five(self):
        if self.rates() <= 4:
            return ''
        if self.rates() > 4:
            if self.rates() < 5:
                return '-half'
            else:
                return '-fill'
    def asin(self):
        return self.upc[:10]
    def capacity_time(self):
        if self.production_capacity_time == timedelta(hours=24):
            return 'one_day'
        if self.production_capacity_time == timedelta(weeks=4):
            return 'one_month'
        if self.production_capacity_time == timedelta(days=365):
            return 'limited_stock'
    def production_capacity(self):
        language = global_request.session.get('language')
        if language == 'en-us':
            if self.production_capacity_time == timedelta(hours=24):
                return str(self.production_capacity_quantity) + ' per day'
            if self.production_capacity_time == timedelta(weeks=4):
                return str(self.production_capacity_quantity) + ' per month'
            if self.production_capacity_time == timedelta(days=365):
                return 'limited stock' + ' (' + str(self.production_capacity_quantity) + ')'
        if language == 'fr-fr':
            if self.production_capacity_time == timedelta(hours=24):
                return str(self.production_capacity_quantity) + ' par jour'
            if self.production_capacity_time == timedelta(weeks=4):
                return str(self.production_capacity_quantity) + ' par mois'
            if self.production_capacity_time == timedelta(days=365):
                return 'stock limité' + ' (' + str(self.production_capacity_quantity) + ')'
        if language == 'ar-dz':
            if self.production_capacity_time == timedelta(hours=24):
                return ' يوميا' + str(self.production_capacity_quantity)
            if self.production_capacity_time == timedelta(weeks=4):
                return ' في الشهر' + str(self.production_capacity_quantity)
            if self.production_capacity_time == timedelta(days=365):
                return  '(' + str(self.production_capacity_quantity) + ') ' + 'كمية محدودة'
# ---------------------------------------------------------------------- #

# ------------------------------- Regular ------------------------------ #
class Variant(models.Model):
    # ----- Technical ----- #
    is_activated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # ----- relations ----- #
    product = models.ForeignKey('management.Product', on_delete=models.CASCADE, null=True)
    # ----- content ----- #
    en_spec = models.CharField(max_length=200, blank=True, null=True)
    fr_spec = models.CharField(max_length=200, blank=True, null=True)
    ar_spec = models.CharField(max_length=200, blank=True, null=True)
    # ----- functions ----- #
    def duplicate(self):
        new_variant = Variant(product = self.product)
        new_variant.save()
        if self.option_set.all().count:
            for o in self.option_set.all():
                o.upc = None
                o.pk = None
                o.save()
                new_variant.option_set.add(o)
        if self.feature_set.all().count:
            for f in self.feature_set.all():
                f.pk = None
                f.save()
                new_variant.feature_set.add(f)
    def activate(self):
        activation = False
        for o in self.option_set.all():
            if o.is_activated:
                activation = True
        self.is_activated = activation
        super().save()
        self.product.activate()
    # ----- variables ----- #
    def spec(self):
        language = global_request.session.get('language')
        if language == 'en-us':
            return self.en_spec
        if language == 'fr-fr':
            return self.fr_spec
        if language == 'ar-dz':
            return self.ar_spec
    def image(self):
        if not self.selected_option().has_image:
            return self.album_set.all().first().image
        else:
            return self.selected_option().image
    def admin_image(self):
        return self.album_set.all().first().image
    def selected_option(self):
        option = self.option_set.all().filter(is_activated=True).first()
        for o in self.option_set.all().filter(is_activated=True):
            if o.rate_by_sales() > option.rate_by_sales():
                option = o
        return option
    def is_new(self):
        if not self.selected_option().reviews.all().count():
            return True
        else:
            return False
    def admin_selected_option(self):
        option = self.option_set.all().first()
        for o in self.option_set.all():
            if o.rate_by_sales() > option.rate_by_sales():
                option = o
        return option
    def dimensions_exists(self):
        if self.feature_set.all().filter(en_name='dimensions').exists():
            return True
        else:
            return False
    def weight_exists(self):
        if self.feature_set.all().filter(en_name='weight').exists():
            return True
        else:
            return False
    def color_exists(self):
        if self.feature_set.all().filter(en_name='color').exists():
            return True
        else:
            return False
    def scent_exists(self):
        if self.feature_set.all().filter(en_name='scent').exists():
            return True
        else:
            return False
    def first_list_features(self):
        if self.feature_set.all().count():
            return self.feature_set.all()[int(self.feature_set.all().count() / 2):self.feature_set.all().count()]
    def second_list_features(self):
        if self.feature_set.all().count():
            return self.feature_set.all()[0:int(self.feature_set.all().count() / 2)]
    def needs_more_photos(self):
        if self.album_set.all().count() < 4:
            return True
        else:
            return False
    def full_album(self):
        if self.album_set.all().count() > 7:
            return True
        else:
            return False
    def has_no_photos(self):
        if not self.album_set.all().count():
            return True
        else:
            return False
    def asin(self):
        return self.selected_option().asin()
#                                                                        #
class Product(models.Model):
    # ----- Technical ----- #
    is_activated = models.BooleanField(default=False)
    # ----- relations ----- #
    store = models.ForeignKey('management.Store', on_delete=models.CASCADE, null=True)
    # ----- content ----- #
    en_title = models.CharField(max_length=200, blank=True, null=True)
    fr_title = models.CharField(max_length=200, blank=True, null=True)
    ar_title = models.CharField(max_length=200, blank=True, null=True)
    # ----- #
    en_description = RichTextUploadingField(config_name='default', blank=True, null=True)
    fr_description = RichTextUploadingField(config_name='default', blank=True, null=True)
    ar_description = RichTextUploadingField(config_name='default', blank=True, null=True)
    # ----- #
    brand = models.CharField(max_length=80, blank=True, null=True)
    # ----- functions ----- #
    def unassign_store(self):
        self.store = None
        super().save()
        for v in self.variant_set.all():
            for o in v.option_set.all():
                o.production_capacity_time = None
                o.production_capacity_quantity = 0
                o.save()
    def activate(self):
        activation = False
        for v in self.variant_set.all():
            if v.is_activated:
                activation = True
        self.is_activated = activation
        super().save()
    def add_tag(self, ta_id):
        tag = Tag.objects.all().get(id=ta_id)
        tag.product.add(self)
    def remove_tag(self, ta_id):
        tag = Tag.objects.all().get(id=ta_id)
        tag.product.remove(self)
    def add_collection(self, co_id):
        collection = Collection.objects.all().get(id=co_id)
        collection.product.add(self)
    def remove_collection(self, co_id):
        collection = Collection.objects.all().get(id=co_id)
        collection.product.remove(self)
    def tags_form_text(self, text):
        for t in text.plit():
            if t.count() < 4:
                if Tag.objects.all().filter(title=t).exists():
                    if not self.tags.filter(title=t).exists():
                        tag = Tag.objects.all().get(title=t)
                        tag.product.add(self)
                else:
                    tag = Tag(title=t)
                    tag.save()
                    tag.product.add(self)
    def collect_tags(self):
        self.tags_form_text(self.en_title)
    # ----- variables ----- #
    def title(self):
        language = global_request.session.get('language')
        if language == 'en-us':
            return self.en_title
        if language == 'fr-fr':
            return self.fr_title
        if language == 'ar-dz':
            return self.ar_title
    def description(self):
        language = global_request.session.get('language')
        if language == 'en-us':
            return self.en_description
        if language == 'fr-fr':
            return self.fr_description
        if language == 'ar-dz':
            return self.ar_description
    def image(self):
        return self.selected_variant().image()
    def status(self):
        value = None
        badge_value = None
        badge_color = None
        if self.selected_variant().selected_option().out_of_stock:
            value = 'out_of_stock'
            language = global_request.session.get('language')
            if language == 'en-us':
                badge_value = 'out of stock'
            if language == 'fr-fr':
                badge_value = 'rupture de stock'
            if language == 'ar-dz':
                badge_value = 'نفاذ المخزون'
            badge_color = 'gray-400'
        elif self.selected_variant().is_new():
            value = 'new'
            language = global_request.session.get('language')
            if language == 'en-us':
                badge_value = 'new'
            if language == 'fr-fr':
                badge_value = 'nouveau'
            if language == 'ar-dz':
                badge_value = 'جديد'
            badge_color = 'danger'
        values = {
            'value': value,
            'badge_value': badge_value,
            'badge_color': badge_color,
        }
        return values
    def selected_variant(self):
        variant = self.variant_set.all().exclude(is_activated=False).first()
        for v in self.variant_set.all().exclude(is_activated=False):
            if v.selected_option().rate_by_sales() > variant.selected_option().rate_by_sales():
                variant = v
        return variant
    def selected_collection(self):
        return self.collections.all().first()
    def unselected_tags(self):
        selected_tags = Tag.objects.all()
        for o_t in self.tags.all():
            selected_tags = selected_tags.exclude(id=o_t.id)
        return selected_tags
    def unselected_collections(self):
        selected_collections = Collection.objects.all()
        for col in self.collections.all():
            selected_collections = selected_collections.exclude(id=col.id)
        return selected_collections
    def related_products(self):
        products_ids = []
        for t in self.tags.all():
            for p in t.product.all().exclude(is_activated=False):
                if not p.id in products_ids:
                    products_ids.append(p.id)
        return Product.objects.all().filter(id__in=products_ids).exclude(id=self.id).order_by('?')[:5]
# ---------------------------------------------------------------------- #

# ----------------------------- Collections ---------------------------- #
class Category(models.Model):
    # ----- Technical ----- #
    is_activated = models.BooleanField(default=False)
    rates = models.IntegerField(default=0)
    # ----- content ----- #
    en_name = models.CharField(max_length=300, blank=True, null=True)
    fr_name = models.CharField(max_length=300, blank=True, null=True)
    ar_name = models.CharField(max_length=300, blank=True, null=True)
    # ----- #
    icon = models.CharField(max_length=300, blank=True, null=True)
    # ----- functions ----- #
    class Meta:
        verbose_name_plural = "Categories"
    def add_collection(self, request):
        Collection(en_name=request.POST.get('en_name', None),
                   fr_name=request.POST.get('fr_name', None),
                   ar_name=request.POST.get('ar_name', None),
                   category=self
                   ).save()
    def activate(self):
        if self.check_activation():
            self.is_activated = True
        else:
            self.is_activated = False
        super().save()
    def deactivate(self):
        self.is_activated = False
        super().save()
    # ----- variables ----- #
    def name(self):
        language = global_request.session.get('language')
        if language == 'en-us':
            return self.en_name
        if language == 'fr-fr':
            return self.fr_name
        if language == 'ar-dz':
            return self.ar_name
    def check_collection_activation(self):
        if not self.collections.all().count():
            return False
        else:
            for c in self.collections.all():
                if c.is_activated:
                    return True
        return False
    def check_activation(self):
        if self.icon and self.fr_name and self.ar_name and self.check_collection_activation():
            return True
        return False
    def first_collection_list(self):
        return self.collections.all().order_by('rate')[:2]
    def second_collection_list(self):
        return self.collections.all().order_by('rate')[2:4]
    def third_collection_list(self):
        return self.collections.all().order_by('rate')[4:6]
#                                                                        #
class Collection(models.Model):
    # ----- Technical ----- #
    is_activated = models.BooleanField(default=False)
    rate = models.IntegerField(default=0)
    sale = models.IntegerField(default=0)
    refund = models.IntegerField(default=0)
    # ----- relations ----- #
    category = models.ForeignKey('management.Category', related_name='collections', on_delete=models.CASCADE, blank=True, null=True)
    product = models.ManyToManyField(Product, related_name='collections', blank=True)
    # ----- content ----- #
    en_name = models.CharField(max_length=300, blank=True, null=True)
    fr_name = models.CharField(max_length=300, blank=True, null=True)
    ar_name = models.CharField(max_length=300, blank=True, null=True)
    # ----- functions ----- #
    def activate(self):
        if self.check_activation():
            self.is_activated = True
            super().save()
    def deactivate(self):
        self.is_activated = False
        super().save()
        self.category.activate()
    # ----- variables ----- #
    def name(self):
        language = global_request.session.get('language')
        if language == 'en-us':
            return self.en_name
        if language == 'fr-fr':
            return self.fr_name
        if language == 'ar-dz':
            return self.ar_name
    def check_activation(self):
        if not self.product.all().count():
            return False
        if not self.fr_name or not self.ar_name:
            return False
        return True
    def all_product(self):
        return self.product.all().filter(is_activated=True)
#                                                                        #
class Tag(models.Model):
    # ----- relations ----- #
    product = models.ManyToManyField(Product, related_name='tags', blank=True)
    # ----- content ----- #
    title = models.CharField(max_length=240, unique=True, null=True)
# ---------------------------------------------------------------------- #

# -------------------------- Special Products -------------------------- #
class Store(models.Model):
    # ----- Technical ----- #
    is_activated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # ----- content ----- #
    name = models.CharField(max_length=200, unique=True, null=True)
    address = models.CharField(max_length=400, blank=True, null=True)
    # ----- #
    en_activity = models.CharField(max_length=300, blank=True, null=True)
    fr_activity = models.CharField(max_length=300, blank=True, null=True)
    ar_activity = models.CharField(max_length=300, blank=True, null=True)
    # ----- functions ----- #
    def activate(self):
        if not self.user.profile_photo or not self.name:
            self.is_activated = False
        else:
            self.is_activated = True
        super().save()
    def deactivate(self):
        for p in self.product_set.all():
            for v in p.variant_set.all():
                v.deactivate()
        self.is_activated = False
        super().save()
    # ----- variables ----- #
    def logo(self):
        return self.user.profile_photo
    def completed_orders(self):
        return self.orders.all().filter(status='completed')
    def all_variants(self):
        variant_ids = []
        for p in self.product_set.all():
            for v in p.variant_set.all():
                variant_ids.append(v.id)
        return Variant.objects.filter(id__in=variant_ids)
    def all_products(self):
        option_ids = []
        for p in self.product_set.all():
            for v in p.variant_set.all():
                for o in v.option_set.all():
                    option_ids.append(o.id)
        return Option.objects.filter(id__in=option_ids)
    def new_products(self):
        option_ids = []
        for p in self.product_set.all():
            for v in p.variant_set.all():
                for o in v.option_set.all():
                    if not o.store_ready():
                        option_ids.append(o.id)
        return Option.objects.filter(id__in=option_ids)
    def balance(self):
        balance = 0
        for o in self.completed_orders():
            balance += o.total_cost()
        for transaction in self.user.wallet.transactions.all():
            if transaction.confirmed:
                if transaction.add:
                    balance += transaction.amount
                else:
                    balance -= transaction.amount
        return balance
    def incomes(self):
        amount = 0
        for o in self.completed_orders():
            amount += o.total_cost()
        return amount
    def sales(self):
        sale = 0
        for o in self.completed_orders():
            sale += 1
        return sale
    def rates(self):
        rate = 0
        for p in self.all_products():
            rate += p.rates()
        return rate
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
