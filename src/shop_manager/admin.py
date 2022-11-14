from django.contrib import admin
from .models import InventoryProduct, ShopProductFeatures


class InventoryProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'get_album', 'sku', 'quantity', 'buy_price', 'get_features')


admin.site.register(InventoryProduct, InventoryProductAdmin)
admin.site.register(ShopProductFeatures)
