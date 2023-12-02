from django.urls import path
from . import views

urlpatterns = [
    path('signup/<str:action>', views.account_signup, name='signup'),
    path('login/<str:action>', views.account_login, name='login'),
    path('logout/', views.account_logout, name='logout'),
    path('edit/profile/<str:action>', views.edit_profile, name='edit-profile'),
    path('change/password/', views.change_password, name='change-password'),



    path('edit/profile/photo/', views.edit_profile_photo, name='edit-profile-photo'),
]
