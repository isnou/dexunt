from django.shortcuts import render, redirect
from .models import InventoryProduct


def manager_dashboard(request, lang):
    if lang == "ar":
        url = "rtl/shop-manager/dashboard.html"
    else:
        url = "ltr/shop-manager/dashboard.html"
    context = {
        'lang': lang,
    }
    return render(request, url, context)


def inventory(request, lang):
    if lang == "ar":
        url = "rtl/shop-manager/inventory.html"
    else:
        url = "ltr/shop-manager/inventory.html"
    context = {
        'lang': lang,
    }
    return render(request, url, context)


def add_product(request, action):
    url = add_product_actions(request, action).get('url')
    lang = add_product_actions(request, action).get('lang')

    context = {
        'lang': lang,
    }
    return render(request, url, context)


def add_product_actions(request, action):
    if action == "ar":
        url = "rtl/shop-manager/add-product.html"
        lang = "ar"
    elif action == 'en_save_general_product_information':
        url = "ltr/shop-manager/inventory.html"
        lang = "en"
        if request.method == 'POST':
            product_name = request.POST.get('product_name', False)
            buy_price = request.POST.get('buy_price', False)
            quantity = request.POST.get('quantity', False)
            new_product = InventoryProduct(product_name=product_name,
                                           buy_price=buy_price,
                                           quantity=quantity,
                                           )
            new_product.save()
    else:
        url = "ltr/shop-manager/add-product.html"
        lang = "en"
    return {
        'url': url,
        'lang': lang,
    }
