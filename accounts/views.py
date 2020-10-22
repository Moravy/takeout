from django.shortcuts import resolve_url
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
import json

# Create your views here.
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from .forms import CustomerForm, RestaurantForm, MenuForm

from .models import Restaurant, Menu, Cart, Order, Customer

from django.contrib.auth.views import LoginView
from django.conf import settings
from collections import defaultdict

from django.contrib.auth.decorators import login_required, user_passes_test
from .decorators import allow_users_group
from django.contrib.auth.models import Group

from .navigation import Navigation
# path ""
# return home


def home(request):
    # directions = Navigation.get_directions("Sydney", "Melbourne")
    # print(directions)
    # import folium


    # m = folium.Map([51.5, -0.25], zoom_start=10)
    # test = folium.Html('<b>Hello world</b>', script=True)
    # popup = folium.Popup(test, max_width=2650)
    # folium.RegularPolygonMarker(location=[51.5, -0.25], popup=popup).add_to(m)
    # m=m._repr_html_() #updated
    # context = {'my_map': m}



    return render(request, "accounts/home.html")


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


@ login_required(login_url="customer_login")
@ allow_users_group(allowed_roles=["customer", "admin"])
def customer_profile(request):
    customer_order = request.user.customer.order_set.exclude(status="Done")
    history_order = request.user.customer.order_set.filter(status="Done")
    context = {
        "history_order": history_order,
        "customer_order": customer_order}
    
    return render(request, "accounts/profile.html",context)

# path "/customer/menu"
# list all the menu from each restaurant


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
    all_order = request.user.restaurant.order_set.filter(status="Pending").order_by("customer_id")
    
    # if there is order change color
    if 0 < len(all_order):
        color = "text-success"
    else:
        color = "text-dark"

    # dictionary the user to their list of order
  
    
    customer = defaultdict(list)
    from django.core.serializers import serialize
    
    print(json.loads(serialize('json', all_order,fields=('nam',''))))
  
    
    for i in all_order:
        customer[i.customer.user.username].append(i)
    customers = dict(customer)
    print(customers)
    context = {
        "customers": customers,
    #     "order_length": order_length,
    #     "color": color,
    #     "menu_list": menu,
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
    elif data["action"] == "coming_status":
        customer=data["customer"]
        list_of_order = request.user.restaurant.order_set.filter(customer__user__username=customer)
        for order in list_of_order:
            order.status = "Coming"
            order.save()

    
    return JsonResponse("Item was added", safe=False)


# LOGINVIEW


class RestaurantLoginView(LoginView):
    template_name = "accounts/restaurant/login.html"

    def get_success_url(self):

        # url = "company/profile/"

        return resolve_url("company_profile")
