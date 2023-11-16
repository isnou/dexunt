from django.forms import ModelForm
from django import forms
from .models import Product ,Variant ,Feature ,Option ,FlashProduct, Store, Category
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
        fields = ('en_value', 'fr_value', 'ar_value', 'upc')

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
        fields = ('name', 'en_activity', 'fr_activity', 'ar_activity', 'address')

class ENProductDescriptionForm(forms.ModelForm):
    en_description = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Product
        fields = ['en_description']

class FRProductDescriptionForm(forms.ModelForm):
    fr_description = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Product
        fields = ['fr_description']

class ARProductDescriptionForm(forms.ModelForm):
    ar_description = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Product
        fields = ['ar_description']

class ProductDescriptionForm(forms.ModelForm):
    en_description = forms.CharField(widget=CKEditorUploadingWidget())
    fr_description = forms.CharField(widget=CKEditorUploadingWidget())
    ar_description = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Product
        fields = ('en_title', 'fr_title', 'ar_title', 'en_description', 'fr_description', 'ar_description')
