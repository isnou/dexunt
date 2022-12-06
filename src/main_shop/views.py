from django.shortcuts import render, redirect


def main_shop_home(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en'
    direction = request.session.get('language')
    url = direction + "/main-shop/base.html"
    context = {
    }
    return render(request, url, context)
