from django.contrib import admin
from .models import ProductAlbum, ProductFeatures, CollectionFeatures, Product, Collection


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'get_album', 'sku', 'upc', 'quantity', 'buy_price', 'get_features')


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'sku', 'get_products', 'tag', 'sel_price', 'discount_price', 'get_features')


class ProductFeaturesAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'value')


admin.site.register(ProductAlbum)
admin.site.register(ProductFeatures, ProductFeaturesAdmin)
admin.site.register(CollectionFeatures)
admin.site.register(Product, ProductAdmin)
admin.site.register(Collection, CollectionAdmin)
