from accounts.models import *
user1 = User.objects.get(username="jo")
cus1 = Customer.objects.get(user=user1)
CustomerProfile.objects.create(user=cus1)
restaurant = Restaurant.objects.get(company_name="mcdonald")
men1 = Menu.objects.get(restaurant=restaurant)
orders = men1.order_set.all()
