from django.shortcuts import render, redirect
from add_ons import functions
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate
from products.models import Product
from products.forms import ProductForm



def home_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    url = direction + "/home/main-page.html"
    login_form = LoginForm()
    signup_form = SignupForm()

    context = {
        'login_form': login_form,
        'signup_form': signup_form,
    }
    return render(request, url, context)


def management_page(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')

    if action == 'statistics':
        url = direction + "/management/admin/statistics.html"
        context = {
            'nav_side': action
        }
        return render(request, url, context)
    if action == 'products':
        url = direction + "/management/admin/products.html"
        all_products = Product.objects.all()
        product_form = ProductForm()
        context = {
            'nav_side': action,
            'show': 'all_products_table',
            'all_products': all_products,
            'product_form': product_form,
        }
        return render(request, url, context)
    if action == 'add_new_product':
        return redirect('home-page')


def change_language(request):
    if request.method == 'POST':
        language = request.POST.get('language', False)
        page = request.POST.get('page', False)
        request.session['language'] = language

        if page == 'home-page':
            return redirect('home-page')