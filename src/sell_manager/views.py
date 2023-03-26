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
        provinces = None
        if cart_actions.add_product_to_cart(request).get('redirecting'):
            url = direction + cart_actions.show_cart(request).get('url')
            provinces = cart_actions.show_cart(request).get('provinces')
        context = {
            'provinces': provinces,
        }
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
        municipality = Municipality.objects.all().get(en_name=municipality_en_name)
        home_delivery_price = checkout_actions.get_shipping_prices(request, municipality_en_name).get('home_delivery_price')
        desk_delivery_price = checkout_actions.get_shipping_prices(request, municipality_en_name).get('desk_delivery_price')
        sub_context = {
            'home_delivery_price': home_delivery_price,
            'desk_delivery_price': desk_delivery_price,
            'municipality': municipality,
        }
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
        cart = Cart.objects.all().get(ref=request.session.get('cart'))
        url = direction + checkout_actions.details(request).get('url')
        earned_points = checkout_actions.details(request).get('earned_points')
        shipping_price = checkout_actions.details(request).get('shipping_price')
        province = checkout_actions.details(request).get('province')
        municipality = checkout_actions.details(request).get('municipality')
        total_price = cart.sub_total_price + shipping_price
        context = {
            'cart': cart,
            'earned_points': earned_points,
            'shipping_price': shipping_price,
            'province': province,
            'municipality': municipality,
            'total_price': total_price,
        }
        return render(request, url, context)


