from django.contrib import admin
from .models import Album, Feature, Product, Collection


class ProductAdmin(admin.ModelAdmin):
    list_display = ('en_product_name', 'en_product_variant_title', 'en_product_variant_value', 'sku', 'upc', 'quantity', 'buy_price')


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('en_product_name', 'sku', 'get_products', 'tag', 'sel_price', 'discount_price', 'get_features')


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'value')


admin.site.register(Album)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Collection, CollectionAdmin)
