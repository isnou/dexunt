from django.urls import path
from . import views

urlpatterns = [
    path('dexunt/', views.home, name="main-shop-home"),
]
