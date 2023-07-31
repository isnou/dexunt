from django.urls import path
from . import views

urlpatterns = [
    # ---- admin ---- #
    path('<str:action>/statistics', views.admin_home, name='admin-manage-home'),
    path('<str:action>/users', views.manage_users, name='admin-manage-users'),
    path('<str:action>/stores', views.manage_stores, name='admin-manage-stores'),
    path('<str:action>/products', views.manage_products, name='admin-manage-products'),
    path('<str:action>/flash', views.manage_flash, name='admin-manage-flash'),
    path('<str:action>/orders', views.manage_orders, name='admin-manage-orders'),
    path('<str:action>/shipping', views.manage_shipping, name='admin-manage-shipping'),
    path('<str:action>/coupon', views.manage_coupon, name='admin-manage-coupon'),
    # ---- customer ---- #
    path('<str:action>/customer/home', views.customer_home, name='customer-home'),
    # ---- provider ---- #
    path('<str:action>/provider/home', views.provider_home, name='provider-home'),
    path('<str:action>/provider/products', views.provider_products, name='provider-products'),
    path('<str:action>/provider/settings', views.provider_settings, name='provider-settings'),
    path('<str:action>/provider/sales', views.provider_sales, name='provider-sales'),
    # ---- seller ---- #
    path('<str:action>/seller/home', views.seller_home, name='seller-home'),
]