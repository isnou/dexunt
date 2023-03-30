from django.contrib import admin
from .models import Cart ,CartProduct ,Province ,Municipality ,Coupon ,Order



admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(CartProduct)
admin.site.register(Province)
admin.site.register(Municipality)
admin.site.register(Coupon)