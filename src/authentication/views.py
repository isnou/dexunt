from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm, UpdateProfileForm, UpdatePhotoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# ---------------------------- renders ---------------------------- #
def account_login(request, action):# (login) #
    session_manager(init=True, source='login')

    if action == 'page':
        url = request.session.get('direction') + "/authentication/login.html"
        if request.session.get('error_messages'):
            errors = request.session.get('error_messages')
            request.session['error_messages'] = None
        else:
            errors = None
        login_form = LoginForm()

        context = {
            'errors': errors,
            'login_form': login_form,
        }
        return render(request, url, context)
    if action == 'auth':
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = authenticate(
                    username=login_form.cleaned_data['username'],
                    password=login_form.cleaned_data['password'],
                )
                if user:
                    login(request, user)
                    return redirect('router')
#                                                                   #
def account_signup(request, action):# (signup) #
    session_manager(init=True, source='signup')

    if action == 'page':

        context = {
        }
        return render(request, url, context)
    if action == 'auth':
        if request.method == 'POST':
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                return redirect('router')
            else:
                request.session['error_messages'] = signup_form.errors
                return redirect('home-page')
        else:
            return redirect('home-page')
#                                                                   #
# ----------------------------------------------------------------- #


@login_required
def account_profile_page(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/account/profile-page.html"

    edit_profile_form = UpdateProfileForm()
    edit_profile_photo_form = UpdateProfilePhotoForm()
    context = {
        'edit_profile_photo_form': edit_profile_photo_form,
        'edit_profile_form': edit_profile_form,
    }
    return render(request, url, context)

@login_required
def edit_profile(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/account/profile-page.html"

    edit_profile_photo_form = UpdateProfilePhotoForm()

    if request.method == 'POST':
        edit_profile_form = UpdateProfileForm(request.POST, instance=request.user)
        if edit_profile_form.is_valid():
            user = edit_profile_form.save()
            login(request, user)
            return redirect('account-profile-page')
        else:
            context = {
                'edit_profile_photo_form': edit_profile_photo_form,
                'edit_profile_form': edit_profile_form,
            }
            return render(request, url, context)

@login_required
def edit_profile_photo(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'

    direction = request.session.get('language')
    url = direction + "/main-shop/account/profile-page.html"

    edit_profile_form = UpdatePhotoForm()

    if request.method == 'POST':
        edit_profile_photo_form = UpdatePhotoForm(request.POST, request.FILES, instance=request.user)
        if edit_profile_photo_form.is_valid():
            user = edit_profile_photo_form.save()
            login(request, user)
            return redirect('account-profile-page')
        else:
            context = {
                'edit_profile_photo_form': edit_profile_photo_form,
                'edit_profile_form': edit_profile_form,
            }
            return render(request, url, context)

@login_required
def change_password(request):
    if not request.session.get('language', None):
        request.session['language'] = 'en'
    direction = request.session.get('language')
    url = direction + "/main-shop/account/change-password.html"

    change_password_form = PasswordChangeForm(user=request.user, data=request.POST or None)
    if change_password_form.is_valid():
        change_password_form.save()
        update_session_auth_hash(request, change_password_form.user)
        return redirect('account-profile-page')

    return render(request, url, {'change_password_form': change_password_form})

def account_logout(request):
    logout(request)
    return redirect('home-page')