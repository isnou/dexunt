from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_shop_home, name='main-shop-home'),
    path('<str:language>/change/language/', views.change_language, name='change-language'),
    path('<str:sku>/<str:size_sku>/single/product/', views.product, name='single-product'),
    path('<str:action>/<int:ref>/grid/shop/', views.grid_shop, name='grid-shop'),
    path('<str:sku>/<str:size_sku>/book/it/', views.book_it, name='book-it'),
]
