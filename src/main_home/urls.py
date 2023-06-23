from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('product/<int:product_id>/<int:option_id>/<str:user_token>/<str:action>', views.product_router, name='product-router'),
    path('cart/<int:product_id>/<int:option_id>/<str:user_token>/<str:action>', views.shopping_cart, name='shopping-cart'),
    path('change/language', views.change_language, name='change-language'),
]