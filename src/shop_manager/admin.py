from django.contrib import admin
from .models import ProductAlbum, InventoryProductFeatures, ShopProductFeatures, InventoryProduct, ShopProduct


class InventoryProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'get_album', 'sku', 'upc', 'quantity', 'buy_price', 'get_features')


class ShopProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'sku', 'get_products', 'tag', 'sel_price', 'discount_price', 'get_features')


admin.site.register(ProductAlbum)
admin.site.register(InventoryProductFeatures)
admin.site.register(ShopProductFeatures)
admin.site.register(InventoryProduct, InventoryProductAdmin)
admin.site.register(ShopProduct, ShopProductAdmin)
