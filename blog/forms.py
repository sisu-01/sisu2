from django import forms
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title','content','visible','tree']

class TreeForm(forms.ModelForm):
    class Meta:
        model = BlogTree
        fields = ['title','seq','parent']
    
    def __init__(self, *args, **kwargs):
        super(TreeForm, self).__init__(*args, **kwargs)
        self.fields['parent'].required = False
