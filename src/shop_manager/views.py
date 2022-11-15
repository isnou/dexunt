from django.shortcuts import render, redirect
from . import actions


def manager_dashboard(request, action):
    if action == "ar":
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
    if action == "ar":
        lang = "ar"
        url = "rtl/shop-manager/inventory.html"
    else:
        lang = "en"
        url = "ltr/shop-manager/inventory.html"
    context = {
        'lang': lang,
        'fool': [0, 1, 2, 3, 4],
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
