from django.contrib.auth.decorators import user_passes_test

def owner_or_employee_required(view_func):
    
    def in_group(user):
        if user.is_authenticated:
            if user.is_superuser:
                return True
            return user.groups.filter(name__in=['Owner', 'Employee']).exists()
        return False
    return user_passes_test(in_group)(view_func)