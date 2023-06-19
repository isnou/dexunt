from django.shortcuts import render, redirect
from add_ons import functions
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate
from main_manager.models import Product, Variant, Option, Feature, Album, FlashProduct
from main_manager.forms import ProductForm, VariantForm, FeatureForm, OptionForm
from authentication.models import User

def home_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    url = direction + "/home/main-page.html"
    login_form = LoginForm()
    signup_form = SignupForm()

    all_products = Product.objects.all()
    all_flash_products = FlashProduct.objects.all()

    published_products = all_products.filter(is_activated=True)
    published_flash_products = all_flash_products.exclude(is_activated=False).order_by('?')[:3]

    context = {
        'login_form': login_form,
        'signup_form': signup_form,
        'published_products': published_products,
        'published_flash_products': published_flash_products,
    }
    return render(request, url, context)

def change_language(request):
    if request.method == 'POST':
        language = request.POST.get('language', False)
        page = request.POST.get('page', False)
        request.session['language'] = language

        if page == 'home-page':
            return redirect('home-page')