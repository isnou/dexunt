from django.urls import path
from . import views

urlpatterns = [
    path('<str:action>/', views.manager_dashboard, name='dashboard'),
    path('<str:action>/inventory/', views.inventory, name='inventory'),
    path('<str:action>/add-product/', views.add_product, name='add-product'),
]