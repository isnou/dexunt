from django import forms
from phonenumber_field.modelfields import PhoneNumberField

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Username')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Password')
    client_name = forms.CharField(max_length=300, label='Name')
    client_phone = forms.PhoneNumberField()