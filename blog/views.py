from django.shortcuts import render
from .models import Menu

# Create your views here.
def index(request):
    temp = Menu.objects.all().order_by('seq')
    result = get_menu_tree(temp)
    context = {
        'menus': result
    }
    return render(request, 'blog/blog.html', context)

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