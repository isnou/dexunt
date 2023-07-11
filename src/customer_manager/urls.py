from django.urls import path
from . import views

urlpatterns = [
    path('<str:action>/statistics', views.customer_home, name='customer-home'),
]