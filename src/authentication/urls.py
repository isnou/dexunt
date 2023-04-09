from django.urls import path
from . import views

urlpatterns = [
    path('login/page/', views.login_page, name='login-page'),
    path('account/orders/page/', views.account_orders_page, name='account-orders-page'),
    path('account/profile/page/', views.account_profile_page, name='account-profile-page'),
    path('account/edit/profile/', views.edit_profile, name='edit-profile'),
    path('account/edit/profile/photo/', views.edit_profile_photo, name='edit-profile-photo'),
    path('account/logout/', views.user_logout, name='user-logout'),
    path('account/signup/', views.signup_page, name='signup-page'),
    path('change/password/', views.change_password, name='change-password'),
]
