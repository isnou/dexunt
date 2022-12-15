from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from .models import Product
from sell_manager.models import Clip
from .models import Layout
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


def product(request, sku):
    try:
        clips = Clip.objects.all()
    except Clip.DoesNotExist:
        raise Http404("No clips")

    if clips.filter(sku=sku).exists():
        clips = clips.filter(sku=sku)
        if clips.filter(type='points-products').exists():
            points_product = clips.get(type='points-products')
        else:
            points_product = None
        if clips.filter(type='delivery-products').exists():
            delivery_product = clips.get(type='delivery-products')
        else:
            delivery_product = None
        if clips.filter(type='solidarity-products').exists():
            solidarity_product = clips.get(type='solidarity-products')
        else:
            solidarity_product = None
    else:
        points_product = None
        delivery_product = None
        solidarity_product = None

    selected_product = Product.objects.all().get(sku=sku)
    related_products = Product.objects.all().filter(en_product_title=selected_product.en_product_title)
    selected_variants = related_products.filter(type='variant')

    album = related_products.filter(type='photo').filter(attach=selected_product.attach)
    size_variants = related_products.filter(type='size').filter(attach=selected_product.attach)

    direction = request.session.get('language')
    url = direction + "/main-shop/product.html"
    context = {
        'selected_product': selected_product,
        'selected_variants': selected_variants,
        'size_variants': size_variants,
        'album': album,
        'points_product': points_product,
        'delivery_product': delivery_product,
        'solidarity_product': solidarity_product,
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
