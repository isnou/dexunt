from django.urls import path
from . import views

urlpatterns = [
    # ---- admin ---- #
    path('admin/home/<str:action>', views.admin_home, name='admin-home'),
]