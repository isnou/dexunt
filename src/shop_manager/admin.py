from django.contrib import admin
from .models import Feature, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('en_product_title', 'type', 'thumb', 'brand', 'model', 'upc', 'sku', 'tag', 'review_rate',
                    'sell_rate', 'quantity', 'buy_price', 'sell_price', 'discount_price', 'get_features')


admin.site.register(Feature)
admin.site.register(Product, ProductAdmin)
