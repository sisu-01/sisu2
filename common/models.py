from django.db import models
from common.utils import ImageUpload

class TopMenu(models.Model):
    url = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20)
    order = models.IntegerField()

    class Meta:
        managed = True
        db_table = 't_top_menu'
        db_table_comment = '최상위 메뉴'

    def __str__(self):
            return self.name
    
class Profile(models.Model):
    nickname = models.CharField(max_length=10)
    desc = models.CharField(max_length=100)
    image = models.ImageField(upload_to=ImageUpload('profile'))

    class Meta:
        managed = True
        db_table = 'profile'
        db_table_comment = '소개'

    def __str__(self):
        return self.nickname

    