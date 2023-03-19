from django.contrib import admin
from .models import Feature, Product, Size, ShowcaseProduct



admin.site.register(Feature)
admin.site.register(Size)
admin.site.register(ShowcaseProduct)
admin.site.register(Product, ProductAdmin)
