from django.shortcuts import render, redirect
from globals.functions import text_selector, session_manager
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate
from authentication.models import User


def home_page(request):
    session_manager()
    direction = request.session.get('direction')

    url = direction + "/home/main.html"


    context = {
        'source_page': 'home-page',
    }
    return render(request, url, context)

def change_language(request):
    language = request.GET.get('language', False)
    source = request.GET.get('source_page', None)

    request.session['language'] = language
    if language == 'ar-dz':
        request.session['direction'] = 'rtl'
    if language == 'en-us' or language == 'fr-fr':
        request.session['direction'] = 'ltr'

    if source == 'home-page':
        return redirect('home-page')



