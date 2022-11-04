from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_shop_home, name="main-shop-home"),
]
