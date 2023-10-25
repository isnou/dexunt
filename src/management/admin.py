from django.contrib import admin
from .models import Product, Variant, Option, Album, Feature, FlashProduct, Store, Review
from .forms import ENProductDescriptionForm, FRProductDescriptionForm, ARProductDescriptionForm


admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(Option)
admin.site.register(Album)
admin.site.register(Feature)
admin.site.register(FlashProduct)
admin.site.register(Store)
admin.site.register(Review)

class ENProductDescriptionAdmin(admin.ModelAdmin):
    form = ENProductDescriptionForm

admin.site.register(Product, ENProductDescriptionAdmin)

class FRProductDescriptionAdmin(admin.ModelAdmin):
    form = FRProductDescriptionForm

admin.site.register(Product, FRProductDescriptionAdmin)

class ARProductDescriptionAdmin(admin.ModelAdmin):
    form = ARProductDescriptionForm

admin.site.register(Product, ARProductDescriptionAdmin)
