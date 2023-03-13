from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from .models import Product
from sell_manager.models import Clip
from shop_manager.models import ShowcaseProduct
from .models import Showcase
from . import grid_shop_actions, product_actions


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
    size_sku = size_sku

    try:
        selected_product = Product.objects.all().get(sku=sku)
    except Product.DoesNotExist:
        raise Http404("Product doesnt exist")

    if ShowcaseProduct.objects.all().filter(en_title=selected_product.en_title).exists():
        selected_variants = ShowcaseProduct.objects.all().filter(en_title=selected_product.en_title)
    else:
        selected_variants = None

    context = {
        'selected_variants': selected_variants,
        'size_sku': size_sku,
    }
    return render(request, url, context)


def grid_shop(request, action, ref):
    direction = request.session.get('language')
    url = direction + "/main-shop/grid-shop.html"

    products = None

    if action == 'all':
        url = direction + grid_shop_actions.all_products(request).get('url')
        products = grid_shop_actions.all_products(request).get('products_list')
    if action == 'showcase':
        url = direction + grid_shop_actions.showcase_products(request, ref).get('url')
        products = grid_shop_actions.showcase_products(request, ref).get('products_list')

    context = {
        'products': products,
    }
    return render(request, url, context)
