from captcha.fields import CaptchaTextInput, CaptchaField
from django import forms
from .models import *

class TreeForm(forms.ModelForm):
    class Meta:
        model = BlogTree
        fields = ['title','seq','parent']
    
    # 이거 있으면 model에서 blank=True 안 해도 form_valid required 없앨 수 있음
    # def __init__(self, *args, **kwargs):
    #     super(TreeForm, self).__init__(*args, **kwargs)
    #     self.fields['parent'].required = False

class PostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title','content','is_public','tree']

class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = 'blog/captcha.html'

class CommentForm(forms.ModelForm):
    captcha = CaptchaField(widget=CustomCaptchaTextInput)
    class Meta:
        model = BlogComment
        fields = ['post','nickname','password','content']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, {})
        if kwargs['user'].is_authenticated and args:
            args[0]['nickname'] = kwargs['user'].first_name
            self.fields['password'].required = False
            self.fields['captcha'].required = False