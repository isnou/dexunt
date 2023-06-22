from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('regular/single/product/<int:product_id>/<str:user_token>', views.regular_single_product, name='regular-single-product-page'),
    path('change/language', views.change_language, name='change-language'),
]