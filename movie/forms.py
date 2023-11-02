from django import forms
from io import BytesIO
from PIL import Image
from .models import *

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title','title_en','brand','location','format','date','poster']

    def __init__(self, *args, **kwargs):
        #MovieForm 선언 할 때 매개변수가 있는가?
        if len(args) > 0:
            #request.FILES에 파일이 있는가?
            if args[1]:
                self.poster = args[1]['poster']
            else:
                self.poster = None

        super(MovieForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(MovieForm, self).save(commit=False)
        #init에서 FILES가 담겼는가?
        if(self.poster):
            import copy
            thumbnail = copy.copy(self.poster)
            temp = self.rescale(thumbnail, 240, 369)
            instance.thumbnail = temp
        if commit:
            instance.save()

        return instance
    
    def rescale(self, data, width, height):
        input_file = BytesIO(data.read())
        img = Image.open(input_file)
        img_width, img_height = img.size
        img_ratio = float(img_width)/float(img_height)
        ratio_w = float(width)/float(height)
        ratio_h = float(height)/float(width)
        if img_ratio < ratio_w:
            blank = int(img_height-(img_width/ratio_w))
            img_height = int(img_width/ratio_w)
            (left, upper, right, lower) = (0, blank//2, img_width, blank//2+img_height)
        else:
            blank = int(img_width-(img_height/ratio_h))
            img_width = int(img_height/ratio_h)
            (left, upper, right, lower) = (blank//2, 0, blank//2+img_width, img_height)
        img = img.crop((left, upper, right, lower))
        img = img.resize((width,height), Image.LANCZOS)
        image_file = BytesIO()
        img.convert('RGB').save(image_file, format='JPEG')
        data.file = image_file
        return data