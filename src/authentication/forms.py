from django import forms
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

class UpdateProfileForm(UserCreationForm):
    first_name = forms.CharField(max_length=300, label='First name')
    last_name = forms.CharField(max_length=300, label='Last name')
    phone_number = PhoneNumberField(blank=True)
    class Meta:
        model = get_user_model()
        fields = ('phone_number', 'first_name', 'last_name')