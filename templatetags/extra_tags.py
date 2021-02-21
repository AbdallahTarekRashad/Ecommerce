from django import template
from django.utils.translation import get_language
from urllib.parse import urlencode
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

register = template.Library()


# Just for define variables in template
@register.simple_tag
def define(val=None):
    return val


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


@register.simple_tag
def rate(num):
    star = '<i class="fa fa-star"></i>'
    half_star = '<i class="fa fa-star-half-o"></i>'
    empty_star = '<i class="fa fa-star-o"></i>'
    result = ''
    for i in range(int(num)):
        result += star
    if num - int(num) >= 0.5:
        result += half_star
        emp = 5 - int(num) - 1
    else:
        emp = 5 - int(num)
    for e in range(emp):
        result += empty_star
    return result


@register.simple_tag
def form_tag(form_field, class_name=None, **kwargs):
    if form_field.field.help_text:
        help_text = '<div data-toggle="tooltip" data-html="true" title="' + str(
            form_field.field.help_text) + '"class="ico-help"><i class="fa fa-question-circle"></i></div>'
    else:
        help_text = ''
    if form_field.field.required:
        label = '<label for="' + str(form_field.name) + '">' + str(
            _(form_field.label)) + '<span style="color:red"> *</span>' + help_text + '</label>'
    else:
        label = '<label for="' + str(form_field.name) + '">' + str(_(form_field.label)) + help_text + '</label>'
    if class_name is None:
        if form_field.errors:
            class_name = 'form-control is-invalid'
        else:
            class_name = 'form-control'
    if form_field.errors:
        error = '<div style="color: red">' + form_field.errors + '</div>'
    else:
        error = ''
    kwargs['class'] = class_name
    form_field.field.widget.attrs.update(kwargs)
    out = label + form_field.__str__() + error
    return mark_safe(out)


@register.simple_tag
def check_tag(form_field):
    dic = {
        'data-bootstrap-switch': '',
        'data-off-color': 'danger',
        'data-on-color': 'success',
    }
    if form_field.field.help_text:
        help_text = '<div title="' + str(
            form_field.field.help_text) + '" data-toggle="tooltip" class="ico-help"><i class="fa fa-question-circle"></i></div>'
    else:
        help_text = ''
    if form_field.field.required:
        label = '<label for="' + str(form_field.name) + '">' + str(
            _(form_field.label)) + '<span style="color:red"> *</span>' + help_text + '</label>'
    else:
        label = '<label for="' + str(form_field.name) + '">' + str(_(form_field.label)) + help_text + '</label>'
    if form_field.errors:
        error = '<div style="color: red">' + form_field.errors + '</div>'
    else:
        error = ''
    form_field.field.widget.attrs.update(dic)
    out = label + '<div style="display: block;width: 100%;text-align: end;">' + form_field.__str__() + '</div>' + error
    return mark_safe(out)

# to return checked if account have permission
@register.simple_tag
def perms(account, permission):
    if account and account.has_perm(permission):
        return 'checked'
    else:
        return ''


# model_name must be in lower case
# app is plural
@register.simple_tag
def perms_row(model_name, app, num, account=None, view=True, add=True, change=True, delete=True):
    number = '<td>' + num + '.</td>'
    class_name = '<td>' + str(_(model_name.capitalize())) + '</td>'
    if view:
        td_view = '<td><input name="' + model_name + '-view" type="checkbox"data-bootstrap-switch ' \
                                                     'data-off-color="danger"data-on-color="success" ' + \
                  perms(account, app + '.view_' + model_name) + '></td> '
    else:
        td_view = '<td></td>'
    if add:
        td_add = '<td><input name="' + model_name + '-add" type="checkbox"data-bootstrap-switch ' \
                                                    'data-off-color="danger"data-on-color="success" ' + \
                 perms(account, app + '.add_' + model_name) + '></td> '
    else:
        td_add = '<td></td>'
    if change:
        td_change = '<td><input name="' + model_name + '-change" type="checkbox"data-bootstrap-switch ' \
                                                       'data-off-color="danger"data-on-color="success" ' + \
                    perms(account, app + '.change_' + model_name) + '></td> '
    else:
        td_change = '<td></td>'
    if delete:
        td_delete = '<td><input name="' + model_name + '-delete" type="checkbox"data-bootstrap-switch ' \
                                                       'data-off-color="danger"data-on-color="success" ' + \
                    perms(account, app + '.delete_' + model_name) + '></td> '
    else:
        td_delete = '<td></td>'

    out = number + class_name + td_view + td_add + td_change + td_delete
    return mark_safe(out)
