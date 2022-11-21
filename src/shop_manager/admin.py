from django.contrib import admin
from .models import Album, Feature, Product, Variant


class ProductAdmin(admin.ModelAdmin):
    list_display = ('en_product_title', 'fr_product_title', 'ar_product_title', 'thumb', 'brand', 'model', 'sku',
                    'get_variants', 'tag', 'rate', 'profile', 'sel_price', 'discount_price', 'get_features')


class VariantAdmin(admin.ModelAdmin):
    list_display = ('type', 'value', 'thumb', 'get_album', 'sku', 'upc', 'quantity', 'buy_price', 'rate')


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'value')


admin.site.register(Album)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(Product, ProductAdmin)






