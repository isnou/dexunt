from django.contrib import admin
from .models import User, Wallet, Transaction, DeliveryAddress

admin.site.register(User)
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(DeliveryAddress)

