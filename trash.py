from accounts.models import *
user1 = User.objects.get(username="joey")
cus1 = Customer.objects.get(user=user1)
CustomerProfile.objects.create(user=cus1)
men1 = Menu.objects.first()
orders = men1.order_set.all()

###################### STILL CHANGING USER ##########################
