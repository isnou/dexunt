from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from .models import CartProduct, Cart, Product
from . import cart_actions
from sell_manager.models import Destination

def cart_home(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/main-page.html"
    destinations = None
    destination = None

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
    if action == 'load_sub_destinations':
        destination_name = request.GET.get('destination')
        destination = Destination.objects.all().get(name=destination_name)
        sub_context = {
            'destination': destination,
        }
        return render(request, '/main-shop/partials/load-sub-destinations.html', sub_context)

    context = {
        'destinations': destinations,
    }
    return render(request, url, context)


