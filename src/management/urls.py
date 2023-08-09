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
    # ---- cash manager ---- #
    path('<str:action>/cash/home', views.cash_home, name='cash-home'),
    # ---- member ---- #
    path('<str:action>/member/orders', views.member_orders, name='member-orders'),
    # ---- customer ---- #
    path('<str:action>/customer/home', views.customer_home, name='customer-home'),
    # ---- provider ---- #
    path('<str:action>/provider/products', views.provider_products, name='provider-products'),
    path('<str:action>/provider/profile', views.provider_profile, name='provider-profile'),
    path('<str:action>/provider/store', views.provider_store, name='provider-store'),
    path('<str:action>/provider/sales', views.provider_sales, name='provider-sales'),
    path('<str:action>/provider/wallet', views.provider_wallet, name='provider-wallet'),
    # ---- seller ---- #
    path('<str:action>/seller/home', views.seller_home, name='seller-home'),
]