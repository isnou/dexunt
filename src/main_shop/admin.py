from django.contrib import admin
from .models import Content


class ContentAdmin(admin.ModelAdmin):
    list_display = ('lang', 'page_title')


admin.site.register(Content, ContentAdmin)
