from accounts.models import *
user1 = User.objects.get(username="joey")
cus1 = Customer.objects.get(user=user1)

orders = cus1.order_set.all()
