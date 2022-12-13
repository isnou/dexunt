from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_shop_home, name='main-shop-home'),
    path('<str:language>/', views.change_language, name='change-language'),
    path('<str:sku>/product/', views.product, name='product'),
    path('<str:action>/<int:ref>/grid-shop/', views.grid_shop, name='grid-shop'),
]
