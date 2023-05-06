from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from authentication.forms import LoginForm, SignupForm, UpdateProfileForm, UpdateProfilePhotoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash



def user_login(request):
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
    paginator = Paginator(orders, 6)
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
def wished_products_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/account/orders-page.html"

    wished_products = request.user.wished.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(wished_products, 2)
    try:
        wished_products = paginator.page(page)
    except PageNotAnInteger:
        wished_products = paginator.page(1)
    except EmptyPage:
        wished_products = paginator.page(paginator.num_pages)


    context = {
        'wished_products': wished_products,
    }
    return render(request, url, context)

@login_required
def booked_products_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/account/booked-products.html"

    booked_products = request.user.booked.all()
    products = Product.objects.all()

    for booked_product in booked_products:
        booked_product.available = False
        if products.filter(sku=booked_product.product_sku).exists():
            product = products.get(sku=booked_product.product_sku)
            if booked_product.size_sku == 'main':
                if product.quantity > 0:
                    booked_product.available = True
            else:
                if product.size.all().filter(sku=booked_product.size_sku).exists():
                    product_size = product.size.all().get(sku=booked_product.size_sku)
                    if product_size.quantity > 0:
                        booked_product.available = True
        booked_product.save()

    page = request.GET.get('page', 1)
    paginator = Paginator(booked_products, 2)
    try:
        booked_products = paginator.page(page)
    except PageNotAnInteger:
        booked_products = paginator.page(1)
    except EmptyPage:
        booked_products = paginator.page(paginator.num_pages)


    context = {
        'booked_products': booked_products,
    }
    return render(request, url, context)

@login_required
def wished_products_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/account/wished-products.html"

    wished_products = request.user.wished.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(wished_products, 2)
    try:
        wished_products = paginator.page(page)
    except PageNotAnInteger:
        wished_products = paginator.page(1)
    except EmptyPage:
        wished_products = paginator.page(paginator.num_pages)

    context = {
        'wished_products': wished_products,
    }
    return render(request, url, context)

@login_required
def account_profile_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/account/profile-page.html"

    edit_profile_form = UpdateProfileForm()
    edit_profile_photo_form = UpdateProfilePhotoForm()
    context = {
        'edit_profile_photo_form': edit_profile_photo_form,
        'edit_profile_form': edit_profile_form,
    }
    return render(request, url, context)

@login_required
def edit_profile(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/account/profile-page.html"

    edit_profile_photo_form = UpdateProfilePhotoForm()

    if request.method == 'POST':
        edit_profile_form = UpdateProfileForm(request.POST, instance=request.user)
        if edit_profile_form.is_valid():
            user = edit_profile_form.save()
            login(request, user)
            return redirect('account-profile-page')
        else:
            context = {
                'edit_profile_photo_form': edit_profile_photo_form,
                'edit_profile_form': edit_profile_form,
            }
            return render(request, url, context)

@login_required
def edit_profile_photo(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/account/profile-page.html"

    edit_profile_form = UpdateProfileForm()

    if request.method == 'POST':
        edit_profile_photo_form = UpdateProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if edit_profile_photo_form.is_valid():
            user = edit_profile_photo_form.save()
            login(request, user)
            return redirect('account-profile-page')
        else:
            context = {
                'edit_profile_photo_form': edit_profile_photo_form,
                'edit_profile_form': edit_profile_form,
            }
            return render(request, url, context)

@login_required
def change_password(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'
    direction = request.session.get('language')
    url = direction + "/main-shop/account/change-password.html"

    change_password_form = PasswordChangeForm(user=request.user, data=request.POST or None)
    if change_password_form.is_valid():
        change_password_form.save()
        update_session_auth_hash(request, change_password_form.user)
        return redirect('account-profile-page')

    return render(request, url, {'change_password_form': change_password_form})

@login_required
def router(request):
    if request.user.role == 'admin':
        return redirect('management-page', 'show')

def user_logout(request):
    logout(request)
    return redirect('home-page')