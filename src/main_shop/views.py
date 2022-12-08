from django.shortcuts import render, redirect


def main_shop_home(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'
    direction = request.session.get('language')
    url = direction + "/main-shop/main-page.html"
    context = {
    }
    return render(request, url, context)


def change_language(request, language):
    if language == 'en':
        request.session['language'] = 'en'
    if language == 'fr':
        request.session['language'] = 'fr'
    if language == 'ar':
        request.session['language'] = 'ar'
    return redirect('main-shop-home')
