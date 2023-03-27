from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from .models import CartProduct, Cart, Product
from . import cart_actions, checkout_actions
from sell_manager.models import Province, Municipality

def cart_home(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')

    if action == 'add_product_to_cart':
        url = direction + cart_actions.add_product_to_cart(request).get('url')
        context = cart_actions.add_product_to_cart(request).get('context')

        return render(request, url, context)

    if action == 'remove_product_from_cart':
        url = direction + cart_actions.remove_product_from_cart(request).get('url')
        context = {
        }
        return render(request, url, context)

    if action == 'remove_quantity':
        url = direction + cart_actions.remove_quantity(request).get('url')
        provinces = cart_actions.show_cart(request).get('provinces')
        context = {
            'provinces': provinces,
        }
        return render(request, url, context)

    if action == 'show_cart':
        url = direction + cart_actions.show_cart(request).get('url')
        provinces = cart_actions.show_cart(request).get('provinces')
        context = {
            'provinces': provinces,
        }
        return render(request, url, context)

    if action == 'load_municipality':
        province_en_name = request.GET.get('province_en_name')
        province = Province.objects.all().get(en_name=province_en_name)
        sub_context = {
            'province': province,
        }
        return render(request, 'en/main-shop/partials/load_municipality.html', sub_context)

    if action == 'load_prices':
        municipality_en_name = request.GET.get('municipality_en_name')
        sub_context = checkout_actions.get_shipping_prices(request, municipality_en_name).get('sub_context')
        return render(request, 'en/main-shop/partials/load_prices.html', sub_context)

def checkout(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')

    if action == 'details':
        url = direction + checkout_actions.details(request).get('url')
        context = checkout_actions.details(request).get('context')
        return render(request, url, context)

    if action == 'review':
        url = direction + checkout_actions.review(request).get('url')
        context = checkout_actions.review(request).get('context')
        return render(request, url, context)


