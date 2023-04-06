from django import forms
from django.core.validators import RegexValidator

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Username')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Password')

class SignupForm(forms.Form):
    client_name = forms.CharField(max_length=300, label='Name')
    client_phone = forms.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
    username = forms.CharField(max_length=63, label='Username')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Password')
