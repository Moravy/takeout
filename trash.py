<<<<<<< HEAD
from accounts.models import *
user1 = User.objects.get(username="joey")
=======
from accounts.models import User, Customer, Restaurant, Menu, CustomerProfile

user1 = User.objects.get(username="jo")
>>>>>>> dc952c55e4714e8fc25f218c97f4684e9d1e7a79
cus1 = Customer.objects.get(user=user1)
CustomerProfile.objects.create(user=cus1)
restaurant = Restaurant.objects.get(company_name="mcdonald")
men1 = Menu.objects.get(restaurant=restaurant)
orders = men1.order_set.all()
