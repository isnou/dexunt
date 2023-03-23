from django.urls import path
from . import views

urlpatterns = [
    path('<str:action>/cart/to/home/', views.cart_home, name='cart-home'),
    path('<str:action>/check/out/', views.checkout, name='checkout'),
]
