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
    path('<str:action>/tags', views.manage_tags, name='admin-manage-tags'),
    # ---- cash manager ---- #
    path('<str:action>/cash/wallet', views.cash_wallet, name='cash-wallet'),
    path('<str:action>/cash/sales', views.cash_sales, name='cash-sales'),
    path('<str:action>/cash/members', views.cash_members, name='cash-members'),
    path('<str:action>/cash/providers', views.cash_providers, name='cash-providers'),
    # ---- member ---- #
    path('<str:action>/member/orders', views.member_orders, name='member-orders'),
    path('<str:action>/member/refunds', views.member_refunds, name='member-refunds'),
    path('<str:action>/member/profile', views.member_profile, name='member-profile'),
    path('<str:action>/member/payments', views.member_payments, name='member-payments'),
    path('<str:action>/member/wallet', views.member_wallet, name='member-wallet'),
    # ---- customer ---- #
    path('<str:action>/customer/orders', views.customer_orders, name='customer-orders'),
    path('<str:action>/customer/transactions', views.customer_transactions, name='customer-transactions'),
    path('<str:action>/customer/settings', views.customer_settings, name='customer-settings'),
    path('<str:action>/customer/address', views.customer_address, name='customer-address'),
    # ---- provider ---- #
    path('<str:action>/provider/products', views.provider_products, name='provider-products'),
    path('<str:action>/provider/profile', views.provider_profile, name='provider-profile'),
    path('<str:action>/provider/store', views.provider_store, name='provider-store'),
    path('<str:action>/provider/sales', views.provider_sales, name='provider-sales'),
    path('<str:action>/provider/wallet', views.provider_wallet, name='provider-wallet'),
    # ---- seller ---- #
    path('<str:action>/seller/home', views.seller_home, name='seller-home'),
]