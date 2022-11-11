from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class ProductAlbum(models.Model):
    # --------------------------------- picture types ------------------------------------------
    PictureType = (
        ('Thumb', 'Thumb'),
        ('ZoomThumb', 'ZoomThumb'),
        ('Album', 'Album'),
    )
    picture_type = models.CharField(max_length=50, choices=PictureType, blank=True, null=True)
    file_name = models.CharField(max_length=500, blank=True, default='product-image')
    # --------------------------------- picture location ----------------------------------------
    picture = models.ImageField(upload_to='shop-manager/product/image/')

    def __str__(self):
        return self.file_name


class InventoryProduct(models.Model):
    # --------------------------------- technical details --------------------------------------
    sku = models.CharField(max_length=200, unique=True, null=True)
    model = models.CharField(max_length=200, blank=True, null=True)
    product_name = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- product details ----------------------------------------
    brand = models.CharField(max_length=150, blank=True, null=True)
    color = models.CharField(max_length=60, blank=True, null=True)
    dimensions = models.CharField(max_length=60, blank=True, null=True)
    weight = models.CharField(max_length=60, blank=True, null=True)
    ProductLabel = (
        ('Customisable', 'Customisable'),
        ('Limited', 'Limited'),
        ('HandMade', 'HandMade'),
        ('Used', 'Used'),
    )
    product_label = models.CharField(max_length=50, choices=ProductLabel, blank=True, null=True)
    # --------------------------------- inventory information ----------------------------------
    quantity = models.IntegerField(default=0)
    buy_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    features = models.TextField(max_length=800, blank=True)
    description = models.TextField(max_length=800, blank=True)
    album = models.ManyToManyField(ProductAlbum, blank=True)

    def __str__(self):
        return self.name


class ShopProduct(models.Model):
    # --------------------------------- technical details --------------------------------------
    sku = models.CharField(max_length=200, unique=True, null=True)
    product = models.ManyToManyField(InventoryProduct, blank=True)
    tag = models.CharField(max_length=500, blank=True, default='tag')
    # --------------------------------- showcase information -----------------------------------
    title = models.CharField(max_length=200)
    sel_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)

    def __str__(self):
        return self.title
