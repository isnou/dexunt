from django.urls import path
from . import views

urlpatterns = [
    path('<str:action>/products', views.manage_products, name='manage-products'),
]