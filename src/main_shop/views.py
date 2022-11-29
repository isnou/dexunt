from django.shortcuts import render, redirect


def main_shop_home(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en'
        request.session['direction'] = 'ltr/'
    lang = request.session.get('language')
    direction = request.session.get('direction')
    url = direction + "main-shop/base.html"
    context = {
        'lang': lang,
    }
    return render(request, url, context)
