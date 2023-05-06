from django.shortcuts import render, redirect
from add_ons import functions
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate



def home_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')
    url = direction + "/home/main-page.html"
    login_form = LoginForm()
    signup_form = SignupForm()

    context = {
        'login_form': login_form,
        'signup_form': signup_form,
    }
    return render(request, url, context)


def management_page(request, action):
    if not request.session.get('language', None):
        request.session['language'] = 'en-us'
    direction = request.session.get('language')

    nav_side = action
    context = {
        'nav_side': nav_side
    }
    
    if action == 'statistics':
        url = direction + "/management/admin/statistics.html"
        return render(request, url, context)


def change_language(request):
    if request.method == 'POST':
        language = request.POST.get('language', False)
        page = request.POST.get('page', False)
        request.session['language'] = language

        if page == 'home-page':
            return redirect('home-page')