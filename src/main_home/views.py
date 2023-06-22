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

    all_products = Variant.objects.all().filter(is_activated=True)[:15]
    all_flash_products = FlashProduct.objects.all().exclude(is_activated=False).order_by('?')[:10]

    for p in all_products:
        p.clean()

    for f in all_flash_products:
        f.clean()

    published_products = all_products[:10]
    published_flash_products = all_flash_products[:4]

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

def product_router(request, product_id, option_id, user_token, action):
    selected_variant = Variant.objects.all().get(id=product_id)
    selected_product = Product.objects.all().get(product_token=selected_variant.product_token)

    if option_id:
        selected_option = Option.objects.all().get(id=option_id)
    else:
        selected_option = None

    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    url = direction + "/home/regular/single-product.html"

    if action == 'regular_product':
        context = {
            'selected_option': selected_option,
            'selected_variant': selected_variant,
            'selected_product': selected_product,
        }
        return render(request, url, context)