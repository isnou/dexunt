from django.urls import path
from . import views

urlpatterns = [

    path('', views.home_page, name='home-page'),
    
    path('change/language', views.change_language, name='change-language'),
    path('router/', views.router, name='router'),
]