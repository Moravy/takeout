from django import forms
from django.contrib.auth.models import User
from .models import Customer, Restaurant


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("address",)
        widgets = {
            'address': forms.TextInput(
                attrs={'placeholder': 'Address', 'id': 'autocomplete', 'type': 'text'}),
        }


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ("company_name", "address")
        widgets = {
            'company_name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'address': forms.TextInput(
                attrs={'placeholder': 'Address'}),
        }
