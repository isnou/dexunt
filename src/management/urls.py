from django.urls import path
from . import views

urlpatterns = [
    # ---- admin ---- #
    path('<str:action>/statistics', views.admin_home, name='admin-manage-home'),
    path('<str:action>/users', views.manage_users, name='admin-manage-users'),
    path('<str:action>/products', views.manage_products, name='admin-manage-products'),
    path('<str:action>/flash', views.manage_flash, name='admin-manage-flash'),
    path('<str:action>/orders', views.manage_orders, name='admin-manage-orders'),
    path('<str:action>/shipping', views.manage_shipping, name='admin-manage-shipping'),
    path('<str:action>/coupon', views.manage_coupon, name='admin-manage-coupon'),
    # ---- customer ---- #
    path('<str:action>/customers/home', views.customer_home, name='customer-manage-home'),
]