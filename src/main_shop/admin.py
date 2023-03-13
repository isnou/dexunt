from django.contrib import admin
from .models import IntroBanner, Intro, Showcase


class IntroBannerAdmin(admin.ModelAdmin):
    list_display = ('en_intro', 'en_title', 'thumb', 'en_description')


admin.site.register(IntroBanner, IntroBannerAdmin)
admin.site.register(Intro)
admin.site.register(Showcase)

