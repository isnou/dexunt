from django.urls import path
from . import views

urlpatterns = [
    path('<str:lang>/', views.manager_dashboard, name='dashboard'),
    path('<str:lang>/inventory/', views.inventory, name='inventory'),
]