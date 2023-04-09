from django.urls import path
from users.views import ChangePasswordView
from . import views

urlpatterns = [
    path('login/page/', views.login_page, name='login-page'),
    path('account/orders/page/', views.account_orders_page, name='account-orders-page'),
    path('account/profile/page/', views.account_profile_page, name='account-profile-page'),
    path('account/edit/profile/', views.edit_profile, name='edit-profile'),
    path('account/logout/', views.user_logout, name='user-logout'),
    path('account/signup/', views.signup_page, name='signup-page'),
    path('change/password/', views.ChangePasswordView, name='change-password'),
]
