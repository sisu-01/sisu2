from django import forms
from .models import *

BRAND_CHOICES = [
    ("CGV", "CGV"),
    ("메가박스", "메가박스"),
    ("롯데시네마", "롯데시네마"),
    ("기타", "기타"),
    ("VOD", "VOD"),
]
class DateInput(forms.DateInput):
    input_type = 'date'

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title','title_en','brand','format','location','date','poster']
        labels = {
            'title': '제목',
            'title_en': '영제',
            'brand': '브?랜!드',
            'format': '포맷',
            'location': '위?치',
            'date': '날?짜',
            'poster': '포스터',
        }
        widgets = {
            'brand': forms.RadioSelect(choices=BRAND_CHOICES, attrs={"class": "special"}),
            'date': DateInput(),
        }

        """
        title   = models.CharField(max_length=100)#제목
    title_en= models.CharField(max_length=100)#영제
    #photo
    #thumbnail
    brand   = models.CharField(max_length=20)##CGV, 메박, 롯데, 기타, VOD brand new!
    format  = models.CharField(max_length=20)#2d 3d imax screenx dolby colorium type->format
    location= models.CharField(max_length=20)#평촌, 코메, 수롯시, 양양영화, 집 place->location
    date    = models.DateField()
        """