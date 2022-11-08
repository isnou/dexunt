from django.shortcuts import render, redirect
from .models import Content


def main_shop_home(request, lang):
    content = Content.objects.all()
    en = content.filter(lang='EN')
    fr = content.filter(lang='FR')
    ar = content.filter(lang='AR')

    if lang == "ar":
        url = "rtl/main-shop/home.html"
    else:
        url = "ltr/main-shop/home.html"
    context = {
        'lang': lang,
        'en': en,
        'fr': fr,
        'ar': ar,
    }

    return render(request, url, context)
