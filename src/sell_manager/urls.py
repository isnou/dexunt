from django.urls import path
from . import views

urlpatterns = [
    path('<str:action>/cart/to/home/', views.cart_home, name='cart-home'),
    path('<str:action>/check/out/', views.checkout, name='checkout'),
    path('<str:action>/place/order/', views.place_order, name='place-order'),
    path('<str:action>/track/order/', views.track_order, name='track-order'),
]
