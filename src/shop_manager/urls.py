from django.urls import path
from . import views

urlpatterns = [
    path('<str:action>/', views.manager_dashboard, name='dashboard'),
    path('<str:action>/<str:sku>/inventory/', views.inventory, name='inventory'),
    path('<str:action>/<str:sku>/<int:identity>/inventory-edit/', views.inventory_edit, name='inventory-edit'),
    path('<str:action>/<str:sku>/<int:identity>/e-shop/', views.e_shop, name='e-shop'),
]
