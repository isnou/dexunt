from django.forms import ModelForm
from django import forms
from .models import Province, Municipality, Coupon

class ProvinceForm(ModelForm):
    class Meta:
        model = Province
        fields = ('en_name', 'fr_name', 'ar_name')

class MunicipalityForm(ModelForm):
    class Meta:
        model = Municipality
        fields = ('en_home_delivery_time', 'fr_home_delivery_time', 'ar_home_delivery_time', 'home_delivery_price',
                  'en_desk_delivery_time', 'fr_desk_delivery_time', 'ar_desk_delivery_time', 'desk_delivery_price',
                  'en_name', 'fr_name', 'ar_name',)

class CouponForm(ModelForm):
    class Meta:
        model = Coupon
        fields = ('type', 'quantity', 'valid_until', 'code', 'value')


