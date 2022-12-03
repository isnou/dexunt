from django.contrib import admin
from .models import Layout


class LayoutAdmin(admin.ModelAdmin):
    list_display = ('en_first_title', 'thumb', 'rank')


admin.site.register(Layout, LayoutAdmin)

