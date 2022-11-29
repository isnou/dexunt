from django.shortcuts import render, redirect


def main_shop_home(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en'
        request.session['url'] = 'ltr/main-shop/base.html'
    lang = request.session.get('language')
    url = request.session.get('url')
    context = {
        'lang': lang,
    }
    return render(request, url, context)
