from django.contrib import admin
from .models import Product, Variant, Option, Album, Feature, FlashProduct


admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(Option)
admin.site.register(Album)
admin.site.register(Feature)
admin.site.register(FlashProduct)