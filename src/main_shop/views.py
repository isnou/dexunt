from django.shortcuts import render, redirect
from django.utils.translation import gettext as _


def main_shop_home(request):
    return render(request, "main-shop/home.html")
