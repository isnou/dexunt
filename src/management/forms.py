from django.forms import ModelForm
from django import forms
from .models import Product ,Variant ,Feature ,Option ,FlashProduct, Description, Store

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('en_title', 'fr_title', 'ar_title', 'brand')

class VariantForm(ModelForm):
    class Meta:
        model = Variant
        fields = ('en_spec', 'fr_spec', 'ar_spec', 'price', 'discount', 'is_activated')

class OptionForm(ModelForm):
    class Meta:
        model = Option
        fields = ('en_value', 'fr_value', 'ar_value', 'cost', 'price', 'discount', 'points', 'upc',
                  'delivery_quotient', 'max_quantity', 'quantity', 'is_activated', 'en_note', 'fr_note', 'ar_note')

class FlashForm(ModelForm):
    class Meta:
        model = FlashProduct
        fields = ('en_title', 'fr_title', 'ar_title', 'en_spec', 'fr_spec', 'ar_spec', 'en_value', 'fr_value',
                  'ar_value', 'image', 'valid_until', 'discount', 'is_activated')

class FeatureForm(ModelForm):
    class Meta:
        model = Feature
        fields = ('en_name', 'fr_name', 'ar_name', 'en_content', 'fr_content', 'ar_content')

class DescriptionForm(ModelForm):
    fr_title = forms.CharField(required=False)
    ar_title = forms.CharField(required=False)
    en_content = forms.TextField(required=False)
    fr_content = forms.TextField(required=False)
    ar_content = forms.TextField(required=False)
    class Meta:
        model = Description
        fields = ('en_title', 'fr_title', 'ar_title', 'en_content', 'fr_content', 'ar_content')

class StoreForm(ModelForm):
    class Meta:
        model = Store
        fields = ('name', 'en_activity', 'fr_activity', 'ar_activity', 'en_description', 'fr_description',
                  'ar_description', 'en_address', 'fr_address', 'ar_address')
