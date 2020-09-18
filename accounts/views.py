
from django.shortcuts import resolve_url
from django.shortcuts import render, redirect
# Create your views here.
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from .forms import CustomerForm, RestaurantForm

from .models import *

from django.contrib.auth.views import LoginView
from django.conf import settings

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
    user_form = UserCreationForm()
    customer_form = CustomerForm()
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user_created = user_form.save()
            username = user_form.cleaned_data.get('username')

            customer_group = Group.objects.get(name='customer')
            customer_group.user_set.add(user_created)
            new_customer = customer_form.save(commit=False)
            new_customer.user = user_created
            new_customer.save()

            messages.success(request, f'Account Created for {username}')
            return redirect('customer_login')
    return render(request, "accounts/register.html", {"user_form": user_form, "customer_form": customer_form})


# path "/customer/profile"
# if not login, redirect to login
# if user not in the allowed_roles, cant view profile


@login_required(login_url='customer_login')
@allow_users_group(allowed_roles=["customer", "admin"])
def customer_profile(request):
    # context = {
    #     "restaurants": Restaurant.objects.all()
    # }
    restaurants = Restaurant.objects.all()
    menu_list = [
        # {
        #name: restaurant.name
        #menu: menu
        #
        # }

    ]

    for restaurant in restaurants:
        menu = Menu.objects.filter(
            restaurant=restaurant)
        menu_list.append({
            'name': restaurant.company_name,
            'address': restaurant.address,
            'menu_name': menu
        })
    context = {"restaurants": menu_list}
    print(menu_list)

    # print(Menu.objects.filter(restaurant=restaurant))
    return render(request, "accounts/profile.html", context)


######################### COMPANY #########################

# path "/customer/register"
# create user, put user in customer group, create customer, and save

def company_register(request):
    user_form = UserCreationForm()
    restaurant_form = RestaurantForm()
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        restaurant_form = RestaurantForm(request.POST)
        if user_form.is_valid() and restaurant_form.is_valid():
            user_created = user_form.save()
            username = user_form.cleaned_data.get('username')

            restaurant_group = Group.objects.get(name='restaurant')
            restaurant_group.user_set.add(user_created)
            new_restaurant = restaurant_form.save(commit=False)
            new_restaurant.user = user_created
            new_restaurant.save()

            messages.success(request, f'Account Created for {username}')
            return redirect('company_login')
    return render(request, "accounts/restaurant/register.html", {"user_form": user_form, "restaurant_form": restaurant_form})


# path "/restaurant/profile"
# if not login, redirect to login
# if user not in the allowed_roles, cant view profile


@login_required(login_url='company_login')
@allow_users_group(allowed_roles=["restaurant", "admin"])
def company_profile(request):
    return render(request, "accounts/restaurant/profile.html")


class RestaurantLoginView(LoginView):
    template_name = 'accounts/restaurant/login.html'

    def get_success_url(self):

        url = 'company/profile/'

        return resolve_url('company_profile')
