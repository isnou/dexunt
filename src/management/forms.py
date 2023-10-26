from django.forms import ModelForm
from django import forms
from .models import Product ,Variant ,Feature ,Option ,FlashProduct, Store
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('en_title', 'fr_title', 'ar_title')

class VariantForm(ModelForm):
    class Meta:
        model = Variant
        fields = ('en_spec', 'fr_spec', 'ar_spec')

class OptionForm(ModelForm):
    upc = forms.CharField(required=False)
    class Meta:
        model = Option
        fields = ('en_value', 'fr_value', 'ar_value', 'cost', 'price', 'discount', 'points', 'delivery_quotient',
                   'upc', 'max_quantity', 'quantity', 'en_note', 'fr_note', 'ar_note')

class FlashForm(ModelForm):
    class Meta:
        model = FlashProduct
        fields = ['valid_until']

class FeatureForm(ModelForm):
    class Meta:
        model = Feature
        fields = ('en_name', 'fr_name', 'ar_name', 'en_content', 'fr_content', 'ar_content')

class StoreForm(ModelForm):
    class Meta:
        model = Store
        fields = ('name', 'en_activity', 'fr_activity', 'ar_activity', 'en_description', 'fr_description',
                  'ar_description', 'en_address', 'fr_address', 'ar_address')

class ENProductDescriptionForm(forms.ModelForm):
    en_description = forms.TextField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Product
        fields = ['en_description']

class FRProductDescriptionForm(forms.ModelForm):
    fr_description = forms.TextField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Product
        fields = ['fr_description']

class ARProductDescriptionForm(forms.ModelForm):
    ar_description = forms.TextField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Product
        fields = ['ar_description']

class ProductDescriptionForm(forms.ModelForm):
    en_description = forms.TextField(widget=CKEditorUploadingWidget())
    fr_description = forms.TextField(widget=CKEditorUploadingWidget())
    ar_description = forms.TextField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Product
        fields = ('en_title', 'fr_title', 'ar_title', 'en_description', 'fr_description', 'ar_description')
