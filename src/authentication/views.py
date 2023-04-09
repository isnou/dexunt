from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from authentication.forms import LoginForm, SignupForm, UpdateProfileForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from . import forms


def login_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/account/login-page.html"

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data['username'],
                password=login_form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('account-orders-page')
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
    url = direction + "/main-shop/account/login-page.html"

    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            return redirect('account-orders-page')
        else:
            login_form = LoginForm()
            signup_form = SignupForm()
            context = {
                'login_form': login_form,
                'signup_form': signup_form,
            }
            return render(request, url, context)

@login_required
def account_orders_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/account/orders-page.html"

    orders = request.user.order.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(orders, 2)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)


    context = {
        'orders': orders,
    }
    return render(request, url, context)

@login_required
def account_profile_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/account/profile-page.html"

    edit_profile_form = UpdateProfileForm()
    context = {
        'edit_profile_form': edit_profile_form,
    }
    return render(request, url, context)

@login_required
def edit_profile(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/account/profile-page.html"

    if request.method == 'POST':
        edit_profile_form = UpdateProfileForm(request.POST, instance=request.user)
        if edit_profile_form.is_valid():
            user = edit_profile_form.save()
            login(request, user)
            return redirect('account-profile-page')
        else:
            context = {
                'edit_profile_form': edit_profile_form,
            }
            return render(request, url, context)

def change_password(request):
    return redirect('main-shop-home')

def user_logout(request):

    logout(request)
    return redirect('main-shop-home')
