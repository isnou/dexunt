from django.urls import path
from . import views

urlpatterns = [
    path('<str:lang>/', views.inventory_manager, name='inventory-manager'),
]