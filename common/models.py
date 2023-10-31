from django.db import models
from common.utils import ImageUpload
    
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

    