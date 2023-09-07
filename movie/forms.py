from django import forms
from io import BytesIO
from PIL import Image as pil
from .models import *

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title','title_en','brand','format','location','date','poster']

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
            #이제 self.poster 을 조리해서 instance.thumbnail 에 넣어주면 컄
            temp = self.rescale(thumbnail, 100, 300, force=True)
            instance.thumbnail = temp
        if commit:
            instance.save()

        return instance
    
    def rescale(self, data, width, height, force=True):
        max_width = width
        max_height = height

        input_file = BytesIO(data.read())
        img = pil.open(input_file)
        if not force:
            img.thumbnail((max_width, max_height), pil.LANCZOS)
        else:
            src_width, src_height = img.size
            src_ratio = float(src_width) / float(src_height)
            dst_width, dst_height = max_width, max_height
            dst_ratio = float(dst_width) / float(dst_height)

            if dst_ratio < src_ratio:
                crop_height = src_height
                crop_width = crop_height * dst_ratio
                x_offset = int(src_width - crop_width) // 2
                y_offset = 0
            else:
                crop_width = src_width
                crop_height = crop_width / dst_ratio
                x_offset = 0
                y_offset = int(src_height - crop_height) // 3
            img = img.crop((x_offset, y_offset, x_offset+int(crop_width), y_offset+int(crop_height)))
            img = img.resize((dst_width, dst_height), pil.LANCZOS)

        image_file = BytesIO()
        img.save(image_file, 'png')
        data.file = image_file
        return data