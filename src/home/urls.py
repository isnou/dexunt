from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('product/<str:action>', views.product_page, name='product-page'),
    path('shop/<str:action>', views.shop_page, name='shop-page'),
    path('shopping/cart/<str:action>', views.shopping_cart_page, name='shopping-cart'),
    path('order/page/<str:action>', views.order_page, name='order-page'),
    path('change/language', views.change_language, name='change-language'),
    path('<str:action>/order/tracking', views.order_tracking, name='order-tracking'),
]