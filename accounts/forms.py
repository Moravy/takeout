from django import forms
# from django.contrib.auth.models import User
from .models import Customer, Restaurant, User


class UserForm(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password", )


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
