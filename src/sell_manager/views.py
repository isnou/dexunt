from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from .models import CartProduct, Cart, Product
from . import cart_actions, checkout_actions
from sell_manager.models import Province

def cart_home(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/main-page.html"
    provinces = None

    if action == 'add_product_to_cart':
        url = direction + cart_actions.add_product_to_cart(request).get('url')
        if cart_actions.add_product_to_cart(request).get('redirecting'):
            action = 'show_cart'
    if action == 'remove_product_from_cart':
        url = direction + cart_actions.remove_product_from_cart(request).get('url')
    if action == 'remove_quantity':
        url = direction + cart_actions.remove_quantity(request).get('url')
        provinces = cart_actions.show_cart(request).get('provinces')
    if action == 'show_cart':
        url = direction + cart_actions.show_cart(request).get('url')
        provinces = cart_actions.show_cart(request).get('provinces')
    if action == 'load_municipality':
        province_en_name = request.GET.get('province_en_name')
        province = Province.objects.all().get(en_name=province_en_name)
        sub_context = {
            'province': province,
        }
        return render(request, 'en/main-shop/partials/load_municipality.html', sub_context)

    context = {
        'provinces': provinces,
    }
    return render(request, url, context)

def checkout(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/checkout-details.html"

    if action == 'details':
        url = direction + checkout_actions.details(request).get('url')
        delivery_quotient = checkout_actions.details(request).get('delivery_quotient')
        context = {
            'delivery_quotient': delivery_quotient,
        }
        return render(request, url, context)


    context = {
    }
    return render(request, url, context)


