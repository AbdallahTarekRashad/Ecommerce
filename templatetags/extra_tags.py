from django import template
from django.utils.translation import get_language
from urllib.parse import urlencode

register = template.Library()


# Just for define variables in template
@register.simple_tag
def define(val=None):
    return val


# to return checked if account have permission
@register.simple_tag
def perms(account, permission):
    if account.has_perm(permission):
        return 'checked'
    else:
        return None


# just if condition to check language
@register.simple_tag
def lang(en, ar):
    # print(get_language())
    if get_language() == 'en' or get_language() == 'en-us':
        return en
    else:
        return ar


@register.simple_tag
def urlparams(*_, **kwargs):
    safe_args = {k: v for k, v in kwargs.items() if v is not None}
    if safe_args:
        return '?{}'.format(urlencode(safe_args))
    return ''
