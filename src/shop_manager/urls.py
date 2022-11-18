from django.urls import path
from . import views

urlpatterns = [
    path('<str:action>/', views.manager_dashboard, name='dashboard'),
    path('<str:action>/inventory/', views.inventory, name='inventory'),
    path('<str:action>/<str:sku>/<int:identity>/inventory-product/', views.inventory_product, name='inventory-product'),
    path('<str:action>/<str:sku>/view-product/', views.view_product, name='view-product'),
    path('<str:action>/<str:sku>/edit-product/', views.edit_product, name='edit-product'),
    path('<str:action>/<str:sku>/delete-product/', views.delete_product, name='delete-product'),
    path('<str:action>/<str:sku>/<int:ident>/delete-option/', views.delete_option, name='delete-option'),
]