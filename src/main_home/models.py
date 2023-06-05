from django.db import models
from main_manager.models import Option
from add_ons import functions

class FlashProduct(models.Model):
    # --------------------------------- product identification ---------------------------------
    en_title = models.CharField(max_length=200, blank=True, null=True)
    fr_title = models.CharField(max_length=200, blank=True, null=True)
    ar_title = models.CharField(max_length=200, blank=True, null=True)
    # --------------------------------- product specs ------------------------------------------
    en_spec = models.CharField(max_length=200, blank=True, null=True)
    fr_spec = models.CharField(max_length=200, blank=True, null=True)
    ar_spec = models.CharField(max_length=200, blank=True, null=True)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    # --------------------------------- media --------------------------------------------------
    def get_image_path(self, filename):
        return self.en_title.lower()

    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    # --------------------------------- technical details --------------------------------------
    valid_until = models.DateTimeField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
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
            self.is_available = False
            super().save()