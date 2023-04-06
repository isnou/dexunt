from django.urls import path
from . import views

urlpatterns = [
    path('login/page/', views.login_page, name='login-page'),
    path('user/page/', views.user_home_page, name='user-home-page'),
    path('logout/', views.logout, name='logout'),
]
