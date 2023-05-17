from django.contrib import admin
from .models import Product, Variant, Option, Album

admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(Option)
admin.site.register(Album)