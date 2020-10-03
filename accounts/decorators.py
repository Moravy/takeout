from django.http import HttpResponse
from django.shortcuts import render, redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return view_func(request, *args, **kwargs)


def allow_users_group(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.last().name
                print(request.user.groups.all())
            if group in allowed_roles:
                print(group in allowed_roles)
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not allow to be here")
            print("********WORKING********", allowed_roles)

        return wrapper_func

    return decorator
