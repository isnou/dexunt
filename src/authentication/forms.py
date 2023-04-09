from django import forms
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Username')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Password')

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('phone_number', 'first_name', 'last_name')

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'phone_number', 'first_name', 'last_name')

class UpdateProfilePhotoForm(forms.ModelForm):
    profile_photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = get_user_model()
        fields = ['profile_photo']
