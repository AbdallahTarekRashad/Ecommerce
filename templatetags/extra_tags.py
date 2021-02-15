from django import template
from django.utils.translation import get_language
from urllib.parse import urlencode
from django.utils.safestring import mark_safe

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
    if get_language() == 'en' or get_language() == 'en-us':
        return en
    else:
        return ar


# For Add get parameter in link link domain.com?age=5&name='abdallah'
@register.simple_tag
def urlparams(*_, **kwargs):
    safe_args = {k: v for k, v in kwargs.items() if v is not None}
    if safe_args:
        return '?{}'.format(urlencode(safe_args))
    return ''


# minus tow number
@register.simple_tag
def minus(first, second):
    return first - second


# plus tow number
@register.simple_tag
def plus(first, second):
    return first + second


# for page href url
@register.simple_tag(takes_context=True)
def page(context, page):
    request = context['request'].GET.copy()
    request._mutable = True
    request.setlist('page', [page])
    request._mutable = False
    return urlparams(**dict(request.items()))


# for price search form to add get url parameter as hidden input to form
@register.simple_tag(takes_context=True)
def price_search(context):
    request = context['request'].GET.copy()
    request._mutable = True
    page = request.get('page', None)
    min = request.get('min', None)
    max = request.get('max', None)
    if page:
        request.pop('page')
    if min:
        request.pop('min')
    if max:
        request.pop('max')
    request._mutable = False
    form_hidden = ''
    dic = dict(request.items())
    for key in dic:
        form_hidden += '<input type="hidden" name="' + key + '" value="' + dic[key] + '">'
    return mark_safe(form_hidden)


# for search form to add get url parameter as hidden input to form
@register.simple_tag(takes_context=True)
def search(context):
    request = context['request'].GET.copy()
    request._mutable = True
    page = request.get('page', None)
    search = request.get('search', None)
    if page:
        request.pop('page')
    if search:
        request.pop('search')
    request._mutable = False
    form_hidden = ''
    dic = dict(request.items())
    for key in dic:
        form_hidden += '<input type="hidden" name="' + key + '" value="' + dic[key] + '">'
    return mark_safe(form_hidden)
