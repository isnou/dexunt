from django.urls import path
from . import views

urlpatterns = [
    path('user/account/login/', views.account_login, name='login'),
    path('user/account/logout/', views.account_logout, name='logout'),
    path('user/account/router/', views.router, name='router'),
    path('account/orders/page/', views.account_orders_page, name='account-orders-page'),
    path('account/profile/page/', views.account_profile_page, name='account-profile-page'),
    path('account/wished/products/page', views.wished_products_page, name='wished-products-page'),
    path('account/booked/products/page', views.booked_products_page, name='booked-products-page'),
    path('account/edit/profile/', views.edit_profile, name='edit-profile'),
    path('account/edit/profile/photo/', views.edit_profile_photo, name='edit-profile-photo'),
    path('change/password/', views.change_password, name='change-password'),
    path('account/signup/', views.account_signup, name='signup'),
]
