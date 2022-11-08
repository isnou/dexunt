from django.shortcuts import render, redirect


def main_shop_home(request, lang):
    if lang == "ar":
        url = "rtl/main-shop/home.html"
    else:
        url = "ltr/main-shop/home.html"
    context = {}
    context['lang'] = lang

    return render(request, url, context)
