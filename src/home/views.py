from django.shortcuts import render, redirect
#from add_ons.functions import serial_number_generator
#from add_ons.variables import get_cart, categories
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate
from authentication.models import User


def home_page(request):

    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    if not request.session.get('direction', None):
        request.session['direction'] = 'ltr'

    direction = request.session.get('direction')

    url = direction + "/home/main.html"


    context = {
        'source_page': 'home-page',
    }
    return render(request, url, context)




