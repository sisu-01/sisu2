from django import template
from blog.models import BlogTree, BlogPost, BlogComment
from movie.models import Movie
from common.models import Profile

register = template.Library()

"""
Blog Base 4형제
"""
@register.simple_tag
def getProfile():
    try:
        profile = Profile.objects.get(id=1)
    except:
        profile = None
    return profile
@register.simple_tag
def getRecentPost():
    try: 
        post = BlogPost.objects.filter().latest('id')
    except:
        post = None
    return post
@register.simple_tag
def getRecentComment():
    cmt_list = BlogComment.objects.filter().order_by('-id')[:2]
    return cmt_list
@register.simple_tag
def getRecentMovie():
    try:
        movie = Movie.objects.filter().latest('id')
    except:
        movie = None
    return movie

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