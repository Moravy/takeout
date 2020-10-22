from django import template
from django.template.defaulttags import register
from accounts.models import Customer
# let template check for group


@register.filter(name="has_group")
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


# let template get the value of the key
# {{dictionary|get_item:key}}


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


# let template get the each value.id in values from keys
# {{dictionary|get_item:key}}


@register.filter
def get_item_id(dictionary, key):
    return [i.id for i in dictionary.get(key)]

@register.filter
def get_customer_name(id):
    return Customer.objects.get(id=id)