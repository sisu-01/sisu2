from django import template
from common.models import TopMenu

register = template.Library()

@register.filter
def weekday(value):
    return ['월','화','수','목','금','토','일'][value]

@register.simple_tag
def top_menu():
    menu = TopMenu.objects.all().order_by('order')
    return menu