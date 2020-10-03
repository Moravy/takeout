from django.shortcuts import resolve_url
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json

# Create your views here.
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from .forms import CustomerForm, RestaurantForm, MenuForm

from .models import Restaurant, Menu, Cart, Order, Customer

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


def register_customer(request):
    user_form = UserCreationForm()
    customer_form = CustomerForm()
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user_created = user_form.save()
            username = user_form.cleaned_data.get("username")

            customer_group = Group.objects.get(name="customer")
            customer_group.user_set.add(user_created)
            new_customer = customer_form.save(commit=False)
            new_customer.user = user_created
            new_customer.save()

            messages.success(request, f"Account Created for {username}")
            return redirect("customer_login")
    return render(
        request,
        "accounts/register.html",
        {"user_form": user_form, "customer_form": customer_form},
    )


# path "/customer/profile"
# if not login, redirect to login
# if user not in the allowed_roles, cant view profile
# Get all the restaurant and its menu


@login_required(login_url="customer_login")
@allow_users_group(allowed_roles=["customer", "admin"])
def customer_profile(request):
    # restaurants = Restaurant.objects.all()
    # menu_list = []
    # for restaurant in restaurants:
    #     menu = Menu.objects.filter(
    #         restaurant=restaurant)
    #     menu_list.append({
    #         'name': restaurant.company_name,
    #         'address': restaurant.address,
    #         'menu_name': menu
    #     })
    # context = {"restaurants": menu_list}
    # print(menu_list)
    return render(request, "accounts/profile.html")


def customer_menu(request):
    restaurants = Restaurant.objects.all()
    menu_list = []
    for restaurant in restaurants:
        menu = Menu.objects.filter(restaurant=restaurant)
        menu_list.append(
            {
                "name": restaurant,
                "address": restaurant.address,
                "menu_name": menu,
            }
        )
    context = {"restaurants": menu_list}
    return render(request, "accounts/menu.html", context)


# path "/customer/cart/"
# list all the item in the card for the user


@login_required(login_url="customer_login")
@allow_users_group(allowed_roles=["customer", "admin"])
def customer_cart(request):
    cart = request.user.customer.cart_set.all()
    context = {"carts": cart}

    return render(request, "accounts/cart.html", context)


######################### COMPANY #########################

# path "/customer/register"
# create user, put user in customer group, create customer, and save


def register_company(request):
    user_form = UserCreationForm()
    restaurant_form = RestaurantForm()
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        restaurant_form = RestaurantForm(request.POST)
        if user_form.is_valid() and restaurant_form.is_valid():
            user_created = user_form.save()
            username = user_form.cleaned_data.get("username")

            restaurant_group = Group.objects.get(name="restaurant")
            restaurant_group.user_set.add(user_created)
            new_restaurant = restaurant_form.save(commit=False)
            new_restaurant.user = user_created
            new_restaurant.save()

            messages.success(request, f"Account Created for {username}")
            return redirect("company_login")
    return render(
        request,
        "accounts/restaurant/register.html",
        {"user_form": user_form, "restaurant_form": restaurant_form},
    )


# path "/restaurant/profile"
# if not login, redirect to login
# if user not in the allowed_roles, cant view profile
# Profile: total order
# Create Menu form
# Get all the customer orders and list them by name


@login_required(login_url="company_login")
@allow_users_group(allowed_roles=["restaurant", "admin"])
def company_profile(request):
    menu = request.user.restaurant.menu_set.all()
    menu_form = MenuForm()
    if request.method == "POST":
        menu_form = MenuForm(request.POST)
        if menu_form.is_valid():
            new_menu = menu_form.save(commit=False)
            new_menu.restaurant = request.user.restaurant
            menu_form.save()
            redirect(company_profile)

    # Get all the restaurant order
    all_order = request.user.restaurant.order_set.all()

    # if there is order change color
    if 0 < len(all_order):
        color = "text-success"
    else:
        color = "text-dark"

    # dictionary the user to their list of order
    from collections import defaultdict

    customer = defaultdict(list)
    order_length = 0
    for i in all_order:
        if i.status == "Pending":
            order_length += 1
            customer[i.customer.user.username].append(i.menu)
    customers = dict(customer)

    context = {
        "customers": customers,
        "order_length": order_length,
        "color": color,
        "menu_list": menu,
        "menu_form": menu_form,
    }
    return render(
        request,
        "accounts/restaurant/profile.html",
        context,
    )


# ALL THE ORDER PROCESS
@login_required(login_url="customer_login")
@allow_users_group(allowed_roles=["restaurant", "customer", "admin"])
def update_order(request):
    data = json.loads(request.body)

    # adding item to cart
    if data["action"] == "add":
        print("adding")
        menu_id = data["menu_id"]
        menu = Menu.objects.get(id=menu_id)
        restaurant = Restaurant.objects.get(menu=menu)
        new_cart_item = Cart(
            menu=menu, restaurant=restaurant, customer=request.user.customer
        )
        new_cart_item.save()

    # delete item from cart
    elif data["action"] == "delete":
        print("deleting")
        # cart_id = data["menu_id"]
        # cart = Cart.objects.get(id=cart_id).delete()
        return redirect("customer_cart")

    # delete menu from restaurant
    elif data["action"] == "delete_menu":
        print("deleting menu")
        menu_id = data["menu_id"]
        Menu.objects.get(id=menu_id).delete()
        return redirect("customer_menu")

    # order item from cart and delete item from cart
    elif data["action"] == "order_item":
        print("ordering")
        all_cart_items = request.user.customer.cart_set.all()
        for item in all_cart_items:
            Cart.objects.get(id=item.id).delete()
            new_order = Order(
                menu=item.menu,
                restaurant=item.restaurant,
                customer=request.user.customer,
            )
            new_order.save()
        return redirect("customer_cart")

    # Changing order status
    elif data["action"] == "delete_order":
        list_of_order = data["menu_id"]
        customer_data = data["customer"]
        user1 = User.objects.get(username=customer_data)
        customer = Customer.objects.get(user=user1)
        list_of_order = [
            i for i in list_of_order if i not in ["[", "]", ",", " "]
        ]
        for i in list_of_order:
            menu = Menu.objects.get(id=i)
            order_status = Order.objects.get(customer=customer, menu=menu)
            order_status.status = "Coming"
            order_status.save()
    return JsonResponse("Item was added", safe=False)


# LOGINVIEW


class RestaurantLoginView(LoginView):
    template_name = "accounts/restaurant/login.html"

    def get_success_url(self):

        # url = "company/profile/"

        return resolve_url("company_profile")
