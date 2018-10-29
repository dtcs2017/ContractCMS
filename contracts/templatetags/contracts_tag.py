from django import template
from decimal import Decimal

register = template.Library()


@register.filter(name='comma')
def total_posts(decimal_obj):
    return "{:,.2f}".format(decimal_obj)


@register.filter(name='rate')
def total_posts(decimal_obj):
    return "{:.2f}%".format(decimal_obj * Decimal('100'))
