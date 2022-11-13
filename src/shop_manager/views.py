from django.shortcuts import render, redirect


def manager_dashboard(request, lang):
    if lang == "ar":
        url = "rtl/shop-manager/dashboard.html"
    else:
        url = "ltr/shop-manager/dashboard.html"
    context = {
        'lang': lang,
    }
    return render(request, url, context)
