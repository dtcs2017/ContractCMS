from django import template
from decimal import Decimal

register = template.Library()


@register.filter(name='comma')
def total_posts(decimal_obj):
    if decimal_obj:
        return "{:,.2f}".format(decimal_obj)
    return ""


@register.filter(name='rate')
def total_posts(decimal_obj):
    if decimal_obj:
        return "{:.2f}%".format(decimal_obj * Decimal('100'))
    return ""


@register.filter(name='show_as_para')
def replace_return_with_br(str_obj):
    return str_obj.replace('\r\n', '<br>').replace('script', 'p')


@register.filter(name='record')
def record(str_obj):
    return str_obj.zfill(4)
