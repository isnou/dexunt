from django.shortcuts import redirect
from functools import wraps


def admin_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff and request.user.is_superuser:
                return function(request, *args, **kwargs)
            else:
                return redirect('router')
        return redirect('login', 'page')
    return wrap