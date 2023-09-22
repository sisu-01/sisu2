from django import template
from common.models import TopMenu
from blog.models import Menu

register = template.Library()

@register.filter
def weekday(value):
    return ['월','화','수','목','금','토','일'][value]

@register.simple_tag
def top_menu():
    menu = TopMenu.objects.all().order_by('order')
    return menu

@register.simple_tag
def getTree():
    menus = Menu.objects.all().order_by('seq')
    return get_menu_tree(menus)

def get_menu_tree(menus, parent=None):
    tree = []
    for menu in menus:
        if menu.id_parent_id == parent:
            child = get_menu_tree(menus, menu.id)
            if child:  
                tree.append({
                    'id': menu.id,
                    'title': menu.title,
                    'child': child,
                })
            else:
                tree.append({
                    'id': menu.id,
                    'title': menu.title,
                })
    return tree