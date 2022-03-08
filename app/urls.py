from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('section/', views.section, name='section'),
    path('product/', views.product, name='product'),
    path('sale/', views.sale, name='sale'),
    path('profile/', views.profile, name='profile'),
]