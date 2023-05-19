from django.forms import ModelForm
from .models import Product ,Variant ,Album ,Feature ,Option

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('en_title', 'fr_title', 'ar_title', 'selected_image', 'brand', 'en_description', 'fr_description', 'ar_description', 'en_note', 'fr_note', 'ar_note', 'price', 'discount', 'variant')

class VariantForm(ModelForm):
    class Meta:
        model = Variant
        fields = ('en_spec', 'fr_spec', 'ar_spec', 'product_token', 'price', 'discount')
