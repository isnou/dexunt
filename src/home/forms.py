from django.forms import ModelForm
from django import forms
from .models import Province, Municipality, Coupon

class ProvinceForm(ModelForm):
    class Meta:
        model = Province
        fields = ('en_name', 'fr_name', 'ar_name', 'home_delivery_price', 'desk_delivery_price')

class MunicipalityForm(ModelForm):
    class Meta:
        model = Municipality
        fields = ('en_name', 'fr_name', 'ar_name', 'home_delivery_price', 'desk_delivery_price')

class CouponForm(ModelForm):
    class Meta:
        model = Coupon
        fields = ('is_subtractive', 'quantity', 'valid_until', 'code', 'value')


