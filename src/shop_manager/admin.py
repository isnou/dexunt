from django.contrib import admin
from .models import Feature, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('en_title', 'type', 'attach', 'thumb', 'brand', 'model', 'upc', 'sku', 'tag', 'review_rate',
                    'sell_rate', 'quantity', 'created_at', 'updated_at', 'buy_price', 'sell_price', 'discount_price',
                    'get_features', 'review_rate', 'sell_rate')


admin.site.register(Feature)
admin.site.register(Product, ProductAdmin)
