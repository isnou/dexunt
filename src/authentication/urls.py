from django.urls import path
from . import views

urlpatterns = [
    path('login/page/', views.user_login, name='user-login'),
    path('account/orders/page/', views.account_orders_page, name='account-orders-page'),
    path('account/profile/page/', views.account_profile_page, name='account-profile-page'),
    path('account/wished/products/page', views.wished_products_page, name='wished-products-page'),
    path('account/booked/products/page', views.booked_products_page, name='booked-products-page'),
    path('account/edit/profile/', views.edit_profile, name='edit-profile'),
    path('account/edit/profile/photo/', views.edit_profile_photo, name='edit-profile-photo'),
    path('change/password/', views.change_password, name='change-password'),
    path('account/logout/', views.user_logout, name='user-logout'),
    path('account/signup/', views.signup_page, name='signup-page'),
]
