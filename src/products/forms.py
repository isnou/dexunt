from django.forms import ModelForm
from .models import Product ,Variant ,Feature ,Option

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('en_title', 'fr_title', 'ar_title', 'selected_image', 'brand', 'en_description', 'fr_description', 'ar_description', 'en_note', 'fr_note', 'ar_note', 'price', 'discount')

class VariantForm(ModelForm):
    class Meta:
        model = Variant
        fields = ('en_spec', 'fr_spec', 'ar_spec', 'price', 'discount')

class FeatureForm(ModelForm):
    class Meta:
        model = Feature
        fields = ('en_title', 'fr_title', 'ar_title', 'en_value', 'fr_value', 'ar_value')

class OptionForm(ModelForm):
    class Meta:
        model = Option