from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Username')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Password')

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'phone_number', 'first_name', 'last_name', 'role')
