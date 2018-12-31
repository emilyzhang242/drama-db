from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='limit')
def limit(arg, value):
    return arg[:value]+"..."

register.filter('limit', limit)