from django.urls import path
from . import views

urlpatterns = [
    path('<str:lang>/', views.inventory_manager, name='inventory-manager'),
    path('<str:lang>/dashboard/', views.dashboard, name='dashboard'),
]