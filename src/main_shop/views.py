from django.shortcuts import render, redirect


def main_shop_home(request):
    return render(request, "main-shop/home.html")
