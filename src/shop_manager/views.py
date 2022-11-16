from django.shortcuts import render, redirect
from . import actions


def manager_dashboard(request, action):
    if action == "ar_dashboard":
        lang = "ar"
        url = "rtl/shop-manager/dashboard.html"
    else:
        lang = "en"
        url = "ltr/shop-manager/dashboard.html"
    context = {
        'lang': lang,
    }
    return render(request, url, context)


def inventory(request, action):
    if action == "ar_product_list_show":
        lang = "ar"
        url = "rtl/shop-manager/inventory.html"
    else:
        lang = "en"
        url = "ltr/shop-manager/inventory.html"
    context = {
        'lang': lang,
    }
    return render(request, url, context)


def add_product(request, action):
    result = actions.add_new_product(request, action)
    lang = result.get('lang')
    url = result.get('url')

    context = {
        'lang': lang,
    }
    return render(request, url, context)


def show_product(request, action, sku):
    result = actions.show(request, action, sku)
    lang = result.get('lang')
    url = result.get('url')
    product_to_show = result.get('product_to_show')

    context = {
        'lang': lang,
        'product_to_show': product_to_show,
    }
    return render(request, url, context)


def edit_product(request, action, sku):
    result = actions.edit(request, action, sku)
    lang = result.get('lang')
    url = result.get('url')
    product_to_edit = result.get('product_to_edit')

    context = {
        'lang': lang,
        'product_to_edit': product_to_edit,
    }
    return render(request, url, context)


def delete_product(request, action, sku):
    result = actions.delete(request, action, sku)
    lang = result.get('lang')
    url = result.get('url')

    context = {
        'lang': lang,
    }
    return render(request, url, context)
