from django import template

register = template.Library()


@register.simple_tag
def define(val=None):
    return val


@register.simple_tag
def perms(account, permission):
    if account.has_perm(permission):
        return 'checked'
    else:
        return None
