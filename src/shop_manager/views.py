from django.shortcuts import render, redirect


def manager_dashboard(request, lang):
    if lang == "ar":
        url = "rtl/manager/base.html"
    else:
        url = "ltr/manager/base.html"
    context = {
        'lang': lang,
    }
    return render(request, url, context)
