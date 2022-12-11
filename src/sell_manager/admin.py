from django.contrib import admin
from .models import Clip


class ClipAdmin(admin.ModelAdmin):
    list_display = ('product_title', 'type', 'en_clip_title', 'en_clip_detail', 'value', 'points')


admin.site.register(Clip, ClipAdmin)
