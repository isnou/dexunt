from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from sell_manager.models import Clip
from shop_manager.models import ShowcaseProduct, Product
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
