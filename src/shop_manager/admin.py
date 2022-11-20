from django.contrib import admin
from .models import ProductAlbum, ProductFeatures, CollectionFeatures, Product, Collection


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'get_album', 'sku', 'upc', 'quantity', 'buy_price', 'get_features')


class ShopProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'sku', 'get_products', 'tag', 'sel_price', 'discount_price', 'get_features')


class ProductFeaturesAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'value')


admin.site.register(ProductAlbum)
admin.site.register(InventoryProductFeatures, InventoryProductFeaturesAdmin)
admin.site.register(ShopProductFeatures)
admin.site.register(Product, ProductAdmin)
admin.site.register(Collection, CollectionAdmin)
