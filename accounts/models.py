from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_restaurant = models.BooleanField(default=False)

# Customer models


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='customer')
    address = models.CharField(max_length=100)

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
