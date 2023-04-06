from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from . import forms


def login_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/login-page.html"

    context = {
    }
    return render(request, url, context)

def user_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/user-page.html"

    context = {
    }
    return render(request, url, context)