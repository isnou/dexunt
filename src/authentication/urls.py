from django.urls import path
from . import views

urlpatterns = [
    path('login/page/', views.login_page, name='login-page'),
    path('user/page/', views.user_home_page, name='user-home-page'),
    path('user/logout/', views.user_logout, name='user-logout'),
    path('signup/page/', views.signup_page, name='signup-page'),

]
