from django.shortcuts import render, redirect


def main_shop_home(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en'
    if action == 'en':
        request.session['language'] = 'en'
    if action == 'fr':
        request.session['language'] = 'fr'
    if action == 'ar':
        request.session['language'] = 'ar'
    direction = request.session.get('language')
    url = direction + "/main-shop/base.html"
    context = {
    }
    return render(request, url, context)
