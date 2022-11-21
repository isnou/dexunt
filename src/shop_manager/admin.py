from django.contrib import admin
from .models import Album, Feature, Product, Collection


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'get_album', 'sku', 'upc', 'quantity', 'buy_price', 'get_features')


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'sku', 'get_products', 'tag', 'sel_price', 'discount_price', 'get_features')


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'value')


admin.site.register(Album)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Collection, CollectionAdmin)
