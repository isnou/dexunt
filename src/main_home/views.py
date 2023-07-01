from django.shortcuts import render, redirect
from add_ons import functions
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate
from .models import Cart, SelectedProduct, get_cart, add_product_to_cart
from .models import Coupon, apply_coupon
from main_manager.models import Product, Variant, Option, Feature, Album, FlashProduct
from main_manager.forms import ProductForm, VariantForm, FeatureForm, OptionForm
from authentication.models import User

def home_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    selected_cart = get_cart(request)
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
        'selected_cart': selected_cart,
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
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')

    if action == 'regular_product':
        url = direction + "/home/regular/single-product.html"

        selected_variant = Variant.objects.all().get(id=product_id)
        selected_product = Product.objects.all().get(product_token=selected_variant.product_token)

        if option_id:
            selected_option = Option.objects.all().get(id=option_id)
        else:
            selected_option = None

        context = {
            'selected_option': selected_option,
            'selected_variant': selected_variant,
            'selected_product': selected_product,
        }
        return render(request, url, context)

def shopping_cart_page(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    selected_cart = get_cart(request)

    coupon_message = request.session.get('coupon_message')
    request.session['coupon_message'] = None

    if action == 'main':
        url = direction + "/home/regular/shopping-cart.html"

        context = {
            'selected_cart': selected_cart,
            'coupon_message': coupon_message,
        }
        return render(request, url, context)

def shopping_cart(request, product_id, option_id, user_token, action):
    selected_cart = get_cart(request)

    if action == 'add_regular_product':
        selected_variant = Variant.objects.all().get(id=product_id)
        selected_option = Option.objects.all().get(id=option_id)
        add_product_to_cart(selected_cart, selected_variant, selected_option)
        return redirect('shopping-cart-page', 'main')

    if action == 'add_quantity':
        selected_product = SelectedProduct.objects.all().get(id=product_id)
        selected_option = Option.objects.all().get(id=selected_product.option_id)
        if selected_option.quantity > selected_product.quantity:
            if selected_option.max_quantity > selected_product.quantity:
                selected_product.quantity += 1
                selected_product.save()
                selected_cart.update_prices()
        return redirect('shopping-cart-page', 'main')

    if action == 'remove_quantity':
        selected_product = SelectedProduct.objects.all().get(id=product_id)
        if selected_product.quantity > 1:
            selected_product.quantity -= 1
            selected_product.save()
            selected_cart.update_prices()
        return redirect('shopping-cart-page', 'main')

    if action == 'delete_product':
        selected_product = SelectedProduct.objects.all().get(id=product_id)
        selected_product.delete()
        selected_cart.update_prices()
        return redirect('shopping-cart-page', 'main')

    if action == 'delete_product_from_home':
        selected_product = SelectedProduct.objects.all().get(id=product_id)
        selected_product.delete()
        selected_cart.update_prices()
        return redirect('home-page')

    if action == 'apply_coupon':
        if request.method == 'POST':
            coupon_code = request.POST.get('coupon_code', False)
            apply_coupon(request, selected_cart, coupon_code)
            return redirect('shopping-cart-page', 'main')
