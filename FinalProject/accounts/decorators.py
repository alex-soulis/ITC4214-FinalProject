# accounts/decorators.py

from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy

def owner_or_employee_required(view_func=None, login_url=None):
    """
    Decorator for views that checks that the user is authenticated and is either
    a superuser or in the 'Owner' or 'Employee' group.
    """
    if login_url is None:
        login_url = reverse_lazy('accounts:login')

    def check(user):
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return user.groups.filter(name__in=['Owner', 'Employee']).exists()

    decorator = user_passes_test(check, login_url=login_url)
    return decorator(view_func) if view_func else decorator


def owner_required(view_func=None, login_url=None):
    """
    Decorator for views that checks that the user is authenticated and is either
    a superuser or in the 'Owner' group.
    """
    if login_url is None:
        login_url = reverse_lazy('accounts:login')

    def check(user):
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return user.groups.filter(name='Owner').exists()

    decorator = user_passes_test(check, login_url=login_url)
    return decorator(view_func) if view_func else decorator
