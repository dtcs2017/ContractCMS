from django import template

register = template.Library()


@register.filter(name='comma')
def total_posts(decimal_obj):
    return "{:,.2f}".format(decimal_obj)
