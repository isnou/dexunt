from django.shortcuts import render, redirect


def main_shop_home(request):
    return render(request, "en/main-shop/home.html")
