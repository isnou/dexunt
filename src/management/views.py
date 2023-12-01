from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from globals.functions import text_selector, session_manager
from authentication.forms import LoginForm, SignupForm
from django.contrib.auth import login, authenticate
from authentication.models import User


# --------------------------- Admin renders ---------------------------- #
@login_required
def admin_home(request, action):
    session_manager(init=True, source='home-page')
    url = request.session.get('direction') + "/management/admin/main.html"

    context = {

        # ------------------------  page title -------------------------- #

        # ------------------------  head banner ------------------------- #

    }
    return render(request, url, context)




