from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='limit')
def limit(arg, value):
    if not arg:
        return ""
    if len(arg) > value:
        return arg[:value]+"..."
    return arg

register.filter('limit', limit)