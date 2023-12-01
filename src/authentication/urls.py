from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.account_signup, name='signup'),
    path('login/<str:action>', views.account_login, name='login'),
    path('logout/', views.account_logout, name='logout'),
    path('change/password/', views.change_password, name='change-password'),


    path('profile/page/', views.account_profile_page, name='account-profile-page'),
    path('edit/profile/', views.edit_profile, name='edit-profile'),
    path('edit/profile/photo/', views.edit_profile_photo, name='edit-profile-photo'),
]
