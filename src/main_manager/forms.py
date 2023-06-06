from django.forms import ModelForm
from django import forms
from .models import Product ,Variant ,Feature ,Option

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('en_title', 'fr_title', 'ar_title', 'selected_image', 'brand', 'en_description', 'fr_description',
                  'ar_description', 'en_note', 'fr_note', 'ar_note', 'price', 'discount', 'is_activated')

class VariantForm(ModelForm):
    class Meta:
        model = Variant
        fields = ('en_spec', 'fr_spec', 'ar_spec', 'price', 'discount', 'is_activated')

class FeatureForm(ModelForm):
    class Meta:
        model = Feature
        fields = ('en_name', 'fr_name', 'ar_name', 'en_content', 'fr_content', 'ar_content')

class OptionForm(ModelForm):
    class Meta:
        model = Option
        fields = ('image', 'en_value', 'fr_value', 'ar_value', 'cost', 'price', 'discount', 'points',
                  'delivery_quotient', 'max_quantity', 'quantity', 'is_activated')
