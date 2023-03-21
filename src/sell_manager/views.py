from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from .models import CartProduct, Cart, Product
from . import cart_actions

def cart_home(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/main-page.html"

    if action == 'add_product_to_cart':
        url = direction + cart_actions.add_product_to_cart(request).get('url')
    if action == 'remove_product_from_cart':
        url = direction + cart_actions.add_product_to_cart(request).get('url')

    context = {
    }
    return render(request, url, context)


