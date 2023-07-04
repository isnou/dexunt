from django.urls import path
from . import views

urlpatterns = [
    path('<str:action>/statistics', views.admin_home, name='admin-home'),
    path('<str:action>/showcase', views.manage_showcase, name='manage-showcase'),
    path('<str:action>/products', views.manage_products, name='manage-products'),
    path('<str:action>/flash', views.manage_flash, name='manage-flash'),
    path('<str:action>/orders', views.manage_orders, name='manage-orders'),
    path('<str:action>/shipping', views.manage_shipping, name='manage-shipping'),
    path('<str:action>/coupon', views.manage_coupon, name='manage-coupon'),
]