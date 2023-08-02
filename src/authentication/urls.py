from django.urls import path
from . import views

urlpatterns = [
    path('user/account/login/', views.account_login, name='login'),
    path('user/account/logout/', views.account_logout, name='logout'),
    path('user/account/router/', views.router, name='router'),
    path('account/profile/page/', views.account_profile_page, name='account-profile-page'),
    path('account/edit/profile/', views.edit_profile, name='edit-profile'),
    path('account/edit/profile/photo/', views.edit_profile_photo, name='edit-profile-photo'),
    path('change/password/', views.change_password, name='change-password'),
    path('account/signup/', views.account_signup, name='signup'),
]
