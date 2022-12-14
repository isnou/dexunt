from django.urls import path
from . import views

urlpatterns = [
    path('<str:action>/', views.manager_dashboard, name='dashboard'),
    path('<str:action>/<str:sku>/inventory/', views.inventory, name='inventory'),
    path('<str:action>/<str:sku>/<int:index>/inventory-edit/', views.inventory_edit, name='inventory-edit'),
    path('<str:action>/<str:detail>/<int:index>/e-shop/', views.e_shop, name='e-shop'),
    path('<str:action>/<str:detail>/<int:index>/e-shop-edit/', views.e_shop_edit, name='e-shop-edit'),
]
