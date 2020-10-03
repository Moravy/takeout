from django import forms
from django.contrib.auth.models import User
from .models import Customer, Restaurant, Menu


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("address",)
        widgets = {
            "address": forms.TextInput(
                attrs={
                    "placeholder": "Address",
                    "id": "autocomplete",
                    "type": "text",
                }
            ),
        }


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ("company_name", "address")
        widgets = {
            "company_name": forms.TextInput(attrs={"placeholder": "Name"}),
            "address": forms.TextInput(attrs={"placeholder": "Address"}),
        }


class MenuForm(forms.ModelForm):
    # name = forms.CharField(label="Food_name")

    class Meta:
        model = Menu
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "name", "size": "50"}
            ),
        }
