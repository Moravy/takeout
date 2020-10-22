from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.


# class User(AbstractUser):
#     is_customer = models.BooleanField(default=False)
#     is_restaurant = models.BooleanField(default=False)

# Customer models


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="customer"
    )
    address = models.CharField(max_length=100)
    image = models.ImageField(
        default="default_male.svg", upload_to="profile_pics"
    )

    def __str__(self):
        return self.user.username


# Restaurant Models


class Restaurant(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="restaurant"
    )
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, null=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=30)
    image = models.ImageField(
        default="default_menu_pic.png", upload_to="menu_pics"
    )

    def __str__(self):
        return self.name


# Order Models


class Cart(models.Model):

    menu = models.ForeignKey(Menu, null=True, on_delete=models.SET_NULL)

    restaurant = models.ForeignKey(
        Restaurant, null=True, on_delete=models.SET_NULL
    )

    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.menu.name


class Order(models.Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Coming", "Coming"),
        ("Done", "Done"),
    )

    menu = models.ForeignKey(Menu, null=True, on_delete=models.SET_NULL)

    restaurant = models.ForeignKey(
        Restaurant, null=True, on_delete=models.SET_NULL
    )

    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL
    )

    status = models.CharField(
        max_length=200,
        null=True,
        choices=STATUS,
        default=("Pending", "Pending"),
    )

    def __str__(self):
        return self.menu.name

