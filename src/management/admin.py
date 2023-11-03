from django.contrib import admin
from .models import Product, Variant, Option, Album, Feature, FlashProduct, Store, Review, Tag
from .forms import ProductDescriptionForm


admin.site.register(Variant)
admin.site.register(Option)
admin.site.register(Album)
admin.site.register(Feature)
admin.site.register(FlashProduct)
admin.site.register(Store)
admin.site.register(Review)
admin.site.register(Tag)

class ProductAdmin(admin.ModelAdmin):
    form = ProductDescriptionForm

admin.site.register(Product, ProductAdmin)
