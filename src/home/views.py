from django.shortcuts import render, redirect
#from add_ons.functions import serial_number_generator
#from add_ons.variables import get_cart, categories
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate
from authentication.models import User


def home_page(request):

    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    if not request.session.get('direction', None):
        request.session['direction'] = 'ltr'

    direction = request.session.get('direction')

    url = direction + "/home/main.html"


    context = {
        'source_page': 'home-page',
    }
    return render(request, url, context)

def change_language(request):
    language = request.GET.get('language', False)
    source = request.GET.get('source_page', None)

    request.session['language'] = language
    if language == 'ar-dz':
        request.session['direction'] = 'rtl'
    if language == 'en-us' or language == 'fr-fr':
        request.session['direction'] = 'ltr'

    if source == 'home-page':
        return redirect('home-page')
    if source == 'product-page':
        return redirect('product-page', 'regular_product')
    if source == 'shopping-cart':
        return redirect('shopping-cart', 'main')
    if source == 'order-page':
        return redirect('order-page', 'main')
    if source == 'grid-shop-page':
        return redirect('shop-page', 'grid')



