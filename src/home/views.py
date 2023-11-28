from django.shortcuts import render, redirect
#from add_ons.functions import serial_number_generator
#from add_ons.variables import get_cart, categories
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate
from authentication.models import User


def home_page(request):
    reset_users()
    selected_cart = get_cart(request)

    if request.user.is_authenticated:
        if request.user.is_provider:
            return redirect('provider-sales', 'main')
        if request.user.is_cash_manager:
            return redirect('cash-wallet', 'main')
        if request.user.is_member:
            return redirect('member-orders', 'main')

    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    if not request.session.get('direction', None):
        request.session['direction'] = 'ltr'
    direction = request.session.get('direction')

    request.session['variant_id'] = None
    request.session['option_id'] = None
    request.session['collection_id'] = None

    url = direction + "/home/main.html"

    if request.session.get('error_messages'):
        errors = request.session.get('error_messages')
        request.session['error_messages'] = None
    else:
        errors = None

    login_form = LoginForm()
    signup_form = SignupForm()

    all_stores = Store.objects.all().filter(is_activated=True).order_by('?')[:6]
    all_products = Product.objects.all().filter(is_activated=True)
    all_flash_products = FlashProduct.objects.all().exclude(is_activated=False).order_by('?')[:10]


    grid_products = all_products
    published_flash_products = all_flash_products[:4]

    context = {
        'source_page': 'home-page',
        'errors': errors,
        'login_form': login_form,
        'signup_form': signup_form,
        'selected_cart': selected_cart,
        'grid_products': grid_products,
        'published_flash_products': published_flash_products,
        'all_stores': all_stores,
        'categories': categories().get('activated'),
    }
    return render(request, url, context)




