from django.urls import path
from . import views

urlpatterns = [
    path('<str:action>/showcase', views.manage_showcase, name='manage-showcase'),
    path('<str:action>/products', views.manage_products, name='manage-products'),
]