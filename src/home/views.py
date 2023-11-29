from django.shortcuts import render, redirect
from globals.functions import text_selector, session_manager
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate
from authentication.models import User


def home_page(request):
    session_manager(init=True, source='home-page')
    url = request.session.get('direction') + "/home/main.html"

    context = {
    }
    return render(request, url, context)

def change_language(request):
    session_manager(language=request.GET.get('language', None))
    return redirect(request.session.get('source', None))




