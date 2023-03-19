from django.contrib import admin
from .models import Feature, Product, Size, ShowcaseProduct, Album


class ProductAdmin(admin.ModelAdmin):
    list_display = ('en_title', 'publish', 'upc', 'sku', 'tag', 'quantity', 'created_at',
                    'updated_at', 'buy_price', 'sell_price', 'discount_price', 'features', 'review_rate', 'sell_rate')


admin.site.register(Album)
admin.site.register(Feature)
admin.site.register(Size)
admin.site.register(ShowcaseProduct)
admin.site.register(Product, ProductAdmin)
