from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from shop_manager.models import ShowcaseProduct, Product
from sell_manager.models import Cart

from .models import Showcase
from . import grid_shop_actions
from add_ons import functions


def main_shop_home(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/main-page.html"

    context = {
    }
    return render(request, url, context)


def change_language(request, language):
    if language == 'en':
        request.session['language'] = 'en'
    if language == 'fr':
        request.session['language'] = 'fr'
    if language == 'ar':
        request.session['language'] = 'ar'
    return redirect('main-shop-home')


def product(request, sku, size_sku):
    direction = request.session.get('language')
    url = direction + "/main-shop/product.html"

    cart = Cart.objects.all().get(ref=request.session.get('cart'))
    selected_product = Product.objects.all().get(sku=sku)

    if ShowcaseProduct.objects.all().filter(en_title=selected_product.en_title).exists():
        variant = ShowcaseProduct.objects.all().get(en_title=selected_product.en_title)
    else:
        variant = None

    if not size_sku == 'main':
        selected_size = selected_product.size.all().get(sku=size_sku)
    else:
        selected_size = None

    if cart.product.all().filter(product_sku=sku).exists():
        if cart.product.all().filter(size_sku=size_sku).exists():
            update = True
        elif size_sku == 'main':
            update = True
        else:
            update = False
    else:
        update=False

    context = {
        'selected_product': selected_product,
        'selected_size': selected_size,
        'variant': variant,
        'size_sku': size_sku,
        'update': update,
    }
    return render(request, url, context)


def grid_shop(request, action, ref):
    direction = request.session.get('language')
    url = direction + "/main-shop/grid-shop.html"

    products = None

    if action == 'all':
        url = direction + grid_shop_actions.all_products(request).get('url')
        products = grid_shop_actions.all_products(request).get('products_list')

    if action == 'best_sellers':
        url = direction + grid_shop_actions.best_sellers(request).get('url')
        products = grid_shop_actions.best_sellers(request).get('products_list')

    if action == 'new_arrivals':
        url = direction + grid_shop_actions.new_arrivals(request).get('url')
        products = grid_shop_actions.new_arrivals(request).get('products_list')

    if action == 'top_rated':
        url = direction + grid_shop_actions.top_rated(request).get('url')
        products = grid_shop_actions.top_rated(request).get('products_list')

    if action == 'showcase':
        url = direction + grid_shop_actions.showcase_products(request, ref).get('url')
        products = grid_shop_actions.showcase_products(request, ref).get('products_list')

    context = {
        'products': products,
    }
    return render(request, url, context)
