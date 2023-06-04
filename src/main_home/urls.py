from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('<str:action>/statistics/menu', views.statistics_menu, name='statistics-menu'),
    path('<str:action>/products/menu', views.products_menu, name='products-menu'),
    path('<str:action>/management/page', views.management_page, name='management-page'),
    path('change/language', views.change_language, name='change-language'),
]