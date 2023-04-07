from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from authentication.forms import LoginForm, SignupForm
from . import forms


def login_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/login-page.html"

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data['username'],
                password=login_form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('user-home-page')
            else:
                login_form = LoginForm()
                signup_form = SignupForm()
                context = {
                    'login_form': login_form,
                    'signup_form': signup_form,
                }
                return render(request, url, context)

def signup_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/login-page.html"

    if request.method == 'POST':
        signup_form = forms.SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            return redirect('user-home-page')
        else:
            login_form = LoginForm()
            signup_form = SignupForm()
            context = {
                'login_form': login_form,
                'signup_form': signup_form,
            }
            return render(request, url, context)

@login_required
def user_home_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/user-home-page.html"

    context = {
    }
    return render(request, url, context)

def user_logout(request):

    logout(request)
    return redirect('main-shop-home')