from django.shortcuts import render, redirect
from .models import Product


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


def product(request, sku):
    selected_product = Product.objects.all().get(sku=sku)
    related_products = Product.objects.all().filter(en_product_title=selected_product.en_product_title)
    selected_variants = related_products.filter(type='main')
    album = related_products.filter(type='photo')
    direction = request.session.get('language')
    url = direction + "/main-shop/product.html"
    context = {
        'selected_product': selected_product,
        'selected_variants': selected_variants,
        'album': album,
    }
    return render(request, url, context)
