from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.core.validators import RegexValidator

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Username')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Password')

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'phone_number', 'first_name', 'last_name')

class PasswordChangeCustomForm(PasswordChangeForm):
    error_css_class = 'has-error'
    error_messages = {'password_incorrect': "Password incorrect."}
    old_password = CharField(required=True, label='Old Password',
                             widget=PasswordInput(attrs={
                                 'class': 'form-control'}),
                             error_messages={
                                 'required': 'Old password required'})
    new_password1 = CharField(required=True, label='Password',
                              widget=PasswordInput(attrs={
                                  'class': 'form-control'}),
                              error_messages={
                                  'required': 'Password required'})
    new_password2 = CharField(required=True, label='Password confirmation',
                              widget=PasswordInput(attrs={
                                  'class': 'form-control'}),
                              error_messages={
                                  'required': 'Confirmation required'})