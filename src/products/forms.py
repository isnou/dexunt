from django.forms import ModelForm
from .models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('en_title', 'fr_title', 'ar_title', 'selected_image', 'brand', 'en_description', 'fr_description', 'ar_description', 'en_note', 'fr_note', 'ar_note', 'price', 'discount')

