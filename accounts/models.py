from django.db import models
from django.contrib.auth.models import AbstractUser, User
# Create your models here.


# class User(AbstractUser):
#     is_customer = models.BooleanField(default=False)
#     is_restaurant = models.BooleanField(default=False)

# Customer models


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='customer')
    address = models.CharField(max_length=100)
    image = models.ImageField(
        default='default_male.svg', upload_to='profile_pics')

    def __str__(self):
        return self.user.username


# Restaurant Models


class Restaurant(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='restaurant')
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='restaurant_menu', null=True)
    name = models.CharField(max_length=30)
    image = models.ImageField(
        default='default_food_pic.png', upload_to='profile_pics')

    def __str__(self):
        return self.name
# Order Models


class Order(models.Model):
    menu = models.ForeignKey(
        Menu, null=True, on_delete=models.SET)
    restaurant = models.ForeignKey(
        Restaurant, null=True, on_delete=models.SET, related_name='customer_order')
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET, related_name='restaurant_order')

    def __str__(self):
        return self.restaurant.company_name
