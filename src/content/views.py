from django.shortcuts import render, redirect
from add_ons import functions


def home_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'

    direction = request.session.get('language')
    url = direction + "/content/home-page.html"

    context = {
    }
    return render(request, url, context)