from django.shortcuts import render, redirect
from . import actions


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
    result = actions.add_product_actions(request, action)
    lang = result.lang
    url = result.url

    context = {
        'lang': lang,
    }
    return render(request, url, context)
