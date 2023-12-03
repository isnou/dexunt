from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm, UpdateProfileForm, UpdatePhotoForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from globals.functions import text_selector, session_manager


# ----------------------------------------------------------------- #
def account_login(request, action):# (login) #
    if action == 'page':
        session_manager(init=True, source='login')
        url = request.session.get('direction') + "/authentication/login.html"
        login_form = LoginForm()

        context = {
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
                    session_manager(message=True, source='login', success=True)
                    return redirect('router')
                else:
                    session_manager(message=True, source='login', login_fail=True)
                    return redirect('router')
#                                                                   #
def account_signup(request, action):# (signup) #
    if action == 'page':
        session_manager(init=True, source='signup')
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
    if action == 'load_username':
        username = request.GET.get('username')

        url = request.session.get('direction') + "/home/partials/signup_username_section.html"
        login_form = LoginForm()
        context = {
            'login_form': login_form,
            'username': username,
        }
        return render(request, url, context)

#                                                                   #
def edit_profile(request, action):# (edit-profile) #
    if action == 'page':
        session_manager(init=True, source='edit-profile')
        url = request.session.get('direction') + "/authentication/edit_profile.html"
        context = {
            # [parent template] --------------------------------------- #

            # [child template] ---------------------------------------- #
            # [child template] -> [title block] ----------------------- #
            'page_title_txt': text_selector(
                en_text="Dexunt | Trusted & Professional Craftsmen Finder | Edit Profile",
                fr_text="Dexunt | Recherche d'Artisans de Confiance et Professionnels | Editer Profil",
                ar_text="ديكسونت | الباحث الموثوق والمحترف عن الحرفيين | تعديل الملف الشخصي",
            ),
        }
        return render(request, url, context)
    if action == 'auth':
        if request.method == 'POST':
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                return redirect('router')
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
def edit_profile_b(request):
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