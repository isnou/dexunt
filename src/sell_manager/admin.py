from django.contrib import admin
from .models import Clip


class ClipAdmin(admin.ModelAdmin):
    list_display = ('sku', 'product_title', 'type', 'en_clip_title', 'value', 'points')


admin.site.register(Clip, ClipAdmin)
