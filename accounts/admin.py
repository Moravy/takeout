from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

from .models import Customer, Restaurant, Menu, Order
# Register your models here.


admin.site.register(Customer)
admin.site.register(Restaurant)


admin.site.register(Menu)
admin.site.register(Order)
