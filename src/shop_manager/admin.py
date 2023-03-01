from django.contrib import admin
from .models import Feature, Product, Collection


class ProductAdmin(admin.ModelAdmin):
    list_display = ('en_title', 'type', 'publish', 'thumb', 'brand', 'model', 'upc', 'sku', 'tag', 'review_rate',
                    'sell_rate', 'quantity', 'created_at', 'updated_at', 'buy_price', 'sell_price', 'discount_price',
                    'get_features', 'review_rate', 'sell_rate')


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('en_title', 'products')


admin.site.register(Feature)
admin.site.register(Product, ProductAdmin)
admin.site.register(Collection, CollectionAdmin)
