from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class ProductAlbum(models.Model):
    # --------------------------------- picture types ------------------------------------------
    Type = (
        ('Thumb', 'Thumb'),
        ('Album', 'Album'),
    )
    type = models.CharField(max_length=50, choices=Type, blank=True, null=True)
    file_name = models.CharField(max_length=500, blank=True, default='product-image')
    # --------------------------------- picture location ---------------------------------------
    picture = models.ImageField(upload_to='shop-manager/product/image/%Y/%m/%d/')

    def __str__(self):
        return self.picture


class InventoryProductFeatures(models.Model):
    # --------------------------------- feature types ------------------------------------------
    Type = (
        ('Model', 'Model'),
        ('Brand', 'Brand'),
        ('Color', 'Color'),
        ('Dimensions', 'Dimensions'),
        ('Size', 'Size'),
        ('Weight', 'Weight'),
    )
    type = models.CharField(max_length=50, choices=Type, blank=True, null=True)
    # --------------------------------- feature language ---------------------------------------
    Language = (
        ('English', 'English'),
        ('French', 'French'),
        ('Arabic', 'Arabic'),
    )
    language = models.CharField(max_length=50, choices=Language, blank=True, null=True)
    # --------------------------------- technical details --------------------------------------
    sku = models.CharField(max_length=20, unique=True, null=True)
    # --------------------------------- feature value ------------------------------------------
    value = models.CharField(max_length=100, unique=True, null=True)

    def __str__(self):
        return self.value


class ShopProductFeatures(models.Model):
    # --------------------------------- feature types ------------------------------------------
    Type = (
        ('Description', 'Description'),
        ('EShopTitle', 'EShopTitle'),
    )
    type = models.CharField(max_length=50, choices=Type, blank=True, null=True)
    # --------------------------------- feature language ---------------------------------------
    Language = (
        ('English', 'English'),
        ('French', 'French'),
        ('Arabic', 'Arabic'),
    )
    language = models.CharField(max_length=50, choices=Language, blank=True, null=True)
    # --------------------------------- feature value ------------------------------------------
    value = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return self.value


class InventoryProduct(models.Model):
    # --------------------------------- product identification ---------------------------------
    product_name = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- media --------------------------------------------------
    album = models.ManyToManyField(ProductAlbum, blank=True)
    # --------------------------------- technical details --------------------------------------
    sku = models.CharField(max_length=20, unique=True, null=True)
    upc = models.CharField(max_length=20, unique=True, null=True)
    quantity = models.IntegerField(default=0)
    buy_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    # --------------------------------- product details ----------------------------------------
    features = models.ManyToManyField(InventoryProductFeatures, blank=True)

    def get_album(self):
        return "\n".join([p.file_name for p in self.album.all()])

    def get_features(self):
        return "\n".join([p.value for p in self.features.all()])

    def __str__(self):
        return self.product_name


class ShopProduct(models.Model):
    # --------------------------------- product identification ---------------------------------
    product_name = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- technical details --------------------------------------
    sku = models.CharField(max_length=20, unique=True, null=True)
    products = models.ManyToManyField(InventoryProduct, blank=True)
    tag = models.CharField(max_length=500, blank=True, default='tag')
    # --------------------------------- showcase information -----------------------------------
    sel_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    features = models.ManyToManyField(ShopProductFeatures, blank=True)

    def get_products(self):
        return "\n".join([p.product_name for p in self.products.all()])

    def get_features(self):
        return "\n".join([p.value for p in self.features.all()])

    def __str__(self):
        return self.product_name
