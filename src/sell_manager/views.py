from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from .models import CartProduct, Cart, Product
from . import cart_actions

def cart_home(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/main-page.html"
    destinations = None
    sub_destinations = None

    if action == 'add_product_to_cart':
        url = direction + cart_actions.add_product_to_cart(request).get('url')
        if cart_actions.add_product_to_cart(request).get('redirecting'):
            action = 'show_cart'
    if action == 'remove_product_from_cart':
        url = direction + cart_actions.remove_product_from_cart(request).get('url')
    if action == 'remove_quantity':
        url = direction + cart_actions.remove_quantity(request).get('url')
    if action == 'show_cart':
        url = direction + cart_actions.show_cart(request).get('url')
        destinations = cart_actions.show_cart(request).get('destinations')
        sub_destinations = cart_actions.show_cart(request).get('sub_destinations')

    context = {
        'destinations': destinations,
        'sub_destinations': sub_destinations,
    }
    return render(request, url, context)


