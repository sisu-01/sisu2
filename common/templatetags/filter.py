from django import template

register = template.Library()

@register.filter
def weekday(value):
    return ['월','화','수','목','금','토','일'][value]