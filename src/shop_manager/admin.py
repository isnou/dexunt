from django.contrib import admin
from .models import Album, Feature, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('en_product_title', 'fr_product_title', 'ar_product_title', 'type', 'value', 'thumb',
                    'brand', 'model', 'upc', 'sku', 'tag', 'review_rate', 'sell_rate', 'quantity', 'buy_price',
                    'sell_price', 'discount_price', 'get_features')


admin.site.register(Feature)
admin.site.register(Product, ProductAdmin)
