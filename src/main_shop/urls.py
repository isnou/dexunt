from django.urls import path
from . import views

urlpatterns = [
    path('<str:action>/home-page', views.main_shop_home, name='main-shop-home'),
]
