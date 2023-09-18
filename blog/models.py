from django.db import models

# Create your models here.
class Menu(models.Model):#이름 바꾸시고
    id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=20)
    id_parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='recomment', null=True)
    seq = models.IntegerField()

    class Meta:
        managed = True
        db_table = 't_blog_menu'
        db_table_comment = '블로그 메뉴'

    def __str__(self):
            return self.title