from django import forms
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.validators import RegexValidator
from phonenumber_field.formfields import PhoneNumberField


class LoginForm(forms.Form):
    username = forms.CharField(max_length=60, label='Username')
    password = forms.CharField(min_length=6, widget=forms.PasswordInput, label='Password')

class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=60)
    password1 = forms.CharField(min_length=6, widget=forms.PasswordInput)
    phone_number = PhoneNumberField(required=False)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'phone_number', 'first_name', 'last_name')

class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    phone_number = PhoneNumberField(required=False)
    class Meta:
        model = get_user_model()
        fields = ('username', 'phone_number', 'first_name', 'last_name')

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username']

class UpdatePhotoForm(forms.ModelForm):
    profile_photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    class Meta:
        model = get_user_model()
        fields = ['profile_photo']
