from django.contrib import admin
from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),

    path('customer/register/', views.customer_register, name='customer_register'),
    path('customer/login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'), name='customer_login'),
    path('customer/logout/', auth_views.LogoutView.as_view(
         template_name='accounts/logout.html'), name='customer_logout'),
    path('customer/profile/', views.customer_profile, name='customer_profile'),


    path('company/register/', views.company_register, name='restaurant_register'),
    path('company/login/', auth_views.LoginView.as_view(
        template_name='accounts/restaurant/login.html'), name='restaurant_login'),

]
