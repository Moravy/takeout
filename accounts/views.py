
from django.shortcuts import render, redirect
# Create your views here.
from .models import User
from .forms import CustomerForm, RestaurantForm, UserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .decorators import allow_users_group


def home(request):
    return render(request, "accounts/base.html")


def in_customer_group(user):
    if user:
        return user.groups.filter(name='customer').count() == 0
    return False


@login_required(login_url='customer_login')
@allow_users_group(allowed_roles=["customer", "admin"])
# @user_passes_test(in_customer_group, login_url='customer_login')
def customer_profile(request):
    return render(request, "accounts/profile.html")


def customer_register(request):
    user_form = UserForm()
    customer_form = CustomerForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if user_form.is_valid():
            new_user = User.objects.create_user(
                **user_form.cleaned_data, is_customer=True)
            username = user_form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}')
            new_restaurant = customer_form.save(commit=False)
            new_restaurant.user = new_user
            new_restaurant.save()
            return redirect('customer_login')
    return render(request, "accounts/register.html", {"user_form": user_form, "customer_form": customer_form})


def company_register(request):
    user_form = UserForm()
    restaurant_form = RestaurantForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        restaurant_form = RestaurantForm(request.POST)
        if user_form.is_valid():
            new_user = User.objects.create_user(
                **user_form.cleaned_data, is_customer=True)
            username = user_form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}')
            new_restaurant = restaurant_form.save(commit=False)
            new_restaurant.user = new_user
            new_restaurant.save()
            # return redirect('customer-login')
    return render(request, "accounts/restaurant/register.html", {"user_form": user_form, "restaurant_form": restaurant_form})
