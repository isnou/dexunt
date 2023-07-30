from django.contrib import admin
from .models import User, Wallet, DeliveryAddress

admin.site.register(User)
admin.site.register(Wallet)
admin.site.register(DeliveryAddress)

