from django.contrib import admin
from django.urls import path


# VIEWS
from . import views
from django.contrib.auth import views as auth_views


# MEDIA SERVING STATIC
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.home, name="home"),
    path(
        "customer/register/", views.register_customer, name="register_customer"
    ),
    path(
        "customer/login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="customer_login",
    ),
    path(
        "customer/logout/",
        auth_views.LogoutView.as_view(template_name="accounts/logout.html"),
        name="customer_logout",
    ),
    path("customer/profile/", views.customer_profile, name="customer_profile"),
    path("customer/menu/", views.customer_menu, name="customer_menu"),
    path("customer/update_order/", views.update_order, name="update_order"),
    path("customer/cart/", views.customer_cart, name="customer_cart"),
    path("company/register/", views.register_company, name="register_company"),
    path(
        "company/login/",
        views.RestaurantLoginView.as_view(
            template_name="accounts/restaurant/login.html"
        ),
        name="company_login",
    ),
    path(
        "company/logout/",
        auth_views.LogoutView.as_view(
            template_name="accounts/restaurant/logout.html"
        ),
        name="company_logout",
    ),
    path("company/profile/", views.company_profile, name="company_profile"),
]

# IF WE ARE IN DEBUGGING MODE
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
