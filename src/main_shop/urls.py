from django.urls import path
from . import views

urlpatterns = [
    path('home-page/', views.main_shop_home, name='main-shop-home'),
    path('<str:language>/', views.change_language, name='change-language'),
]
