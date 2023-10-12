from django import template
from blog.models import BlogTree

register = template.Library()

@register.simple_tag
def getTree():
    menus = BlogTree.objects.all().order_by('seq')
    return get_menu_tree(menus)

@register.simple_tag
def getTree2():
    menus = BlogTree.objects.all().order_by('seq')
    return menus

def get_menu_tree(menus, parent=None):
    tree = []
    for menu in menus:
        if menu.parent_id == parent:
            child = get_menu_tree(menus, menu.id)
            if child:  
                tree.append({
                    'id': menu.id,
                    'title': menu.title,
                    'seq': menu.seq,
                    'child': child,
                })
            else:
                tree.append({
                    'id': menu.id,
                    'title': menu.title,
                    'seq': menu.seq,
                })
    return tree