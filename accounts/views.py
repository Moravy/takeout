
from django.shortcuts import render, redirect
# Create your views here.
from django.contrib.auth.models import AbstractUser, User
from .forms import CustomerForm, RestaurantForm, UserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .decorators import allow_users_group
from django.contrib.auth.models import Group

# path ""
# return home


def home(request):
    return render(request, "accounts/base.html")

######################### CUSTOMER #########################

# path "/customer/register"
# create user, put user in customer group, create customer, and save


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
            customer_group = Group.objects.get(name='customer')
            customer_group.user_set.add(new_user)
            new_restaurant = customer_form.save(commit=False)
            new_restaurant.user = new_user
            new_restaurant.save()
            return redirect('customer_login')
    return render(request, "accounts/register.html", {"user_form": user_form, "customer_form": customer_form})

# path "/customer/profile"
# if not login, redirect to login
# if user not in the allowed_roles, cant view profile


@login_required(login_url='customer_login')
@allow_users_group(allowed_roles=["customer", "admin"])
def customer_profile(request):
    return render(request, "accounts/profile.html")


######################### COMPANY #########################

# path "/customer/register"
# create user, put user in customer group, create customer, and save

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
            restaurant_group = Group.objects.get(name='restaurant')
            restaurant_group.user_set.add(new_user)
            new_restaurant = restaurant_form.save(commit=False)
            new_restaurant.user = new_user
            new_restaurant.save()
            return redirect('company_login')
    return render(request, "accounts/restaurant/register.html", {"user_form": user_form, "restaurant_form": restaurant_form})


# path "/restaurant/profile"
# if not login, redirect to login
# if user not in the allowed_roles, cant view profile

@login_required(login_url='company_login')
@allow_users_group(allowed_roles=["restaurant", "admin"])
def company_profile(request):
    return render(request, "accounts/restaurant/profile.html")
