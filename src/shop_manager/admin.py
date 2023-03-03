from django.contrib import admin
from .models import Feature, Product, Size


class ProductAdmin(admin.ModelAdmin):
    list_display = ('en_title', 'publish', 'upc', 'sku', 'tag', 'sizes', 'quantity', 'created_at',
                    'updated_at', 'buy_price', 'sell_price', 'discount_price', 'features', 'review_rate', 'sell_rate')


admin.site.register(Feature)
admin.site.register(Size)
admin.site.register(Product, ProductAdmin)
