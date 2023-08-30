from django.db import models

# Create your models here.
class Movie(models.Model):
    title   = models.CharField(max_length=100)#제목
    title_en= models.CharField(max_length=100)#영제
    #photo
    #thumbnail
    brand   = models.CharField(max_length=20)##CGV, 메박, 롯데, 기타, VOD brand new!
    format  = models.CharField(max_length=20)#2d 3d imax screenx dolby colorium type->format
    location= models.CharField(max_length=20)#평촌, 코메, 수롯시, 양양영화, 집 place->location
    date    = models.DateField()
    weekday = models.IntegerField()#0월1화2수...5토6일
    #user
    insert_date = models.DateTimeField()
    insert_ip = models.CharField(max_length=40)
    update_date = models.DateTimeField(blank=True, null=True)
    update_ip = models.CharField(max_length=40, blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 't_movie'
        db_table_comment = '영화 기록'
        #indexes로 인덱스 정의 할 수 있다는데 아직 인덱스가 뭔지 잘 몰라.
        #안하면 s 붙여버림;;
        #verbose_name = "t_movie2" -> t_movie2s 
        #verbose_name_plural ='t_movie3' -> t_movie3

    def __str__(self):
            return self.title