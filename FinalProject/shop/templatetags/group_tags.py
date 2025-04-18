from django import template

register = template.Library()

@register.filter
def in_group(user, group_name):
    """Returns True if the given user is in the named group."""
    if not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()
