from django.shortcuts import render, redirect


def inventory_manager(request, lang):
    if lang == "ar":
        url = "rtl/manager/base.html"
    else:
        url = "ltr/manager/base.html"
    context = {
        'lang': lang,
    }
    return render(request, url, context)


def dashboard(request, lang):
    if lang == "ar":
        url = "rtl/manager/dashboard.html"
    else:
        url = "ltr/manager/dashboard.html"
    context = {
        'lang': lang,
    }
    return render(request, url, context)
