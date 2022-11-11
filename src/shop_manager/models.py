from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class ProductAlbum(models.Model):
    # --------------------------------- picture types ------------------------------------------
    PictureType = (
        ('Thumb', 'Thumb'),
        ('ZoomThumb', 'ZoomThumb'),
        ('Album', 'Album'),
    )
    file_name = models.CharField(max_length=500, blank=True, default='product-image')
    picture_type = models.CharField(max_length=50, choices=PictureType, blank=True, null=True)
    # --------------------------------- picture location ----------------------------------------
    picture = models.ImageField(upload_to='shop-manager/images/')

    def __str__(self):
        return self.file_name


class InventoryProduct(models.Model):
    # --------------------------------- technical details --------------------------------------
    sku = models.CharField(max_length=200, unique=True, blank=True, null=True)
    model = models.CharField(max_length=200, blank=True, null=True)
    tag = models.CharField(max_length=500, blank=True, default='tag')
    # --------------------------------- identification details ---------------------------------
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=150)
    # --------------------------------- inventory information ----------------------------------
    quantity = models.IntegerField(default=0)
    buy_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    features = models.TextField(max_length=800, blank=True)
    description = models.TextField(max_length=800, blank=True)
    photo = models.ManyToManyField(ProductAlbum, blank=True)

    def __str__(self):
        return self.name
