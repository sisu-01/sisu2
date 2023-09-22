from django.db import models

# Create your models here.
class Menu(models.Model):
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
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    visible = models.BooleanField()
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True)
    #views = models.IntegerField()
    insert_date = models.DateTimeField()
    insert_ip = models.CharField(max_length=40)
    update_date = models.DateTimeField(blank=True, null=True)
    update_ip = models.CharField(max_length=40, blank=True, null=True)
    """
    썸네일
    댓글수
    """
    class Meta:
        managed = True
        db_table = 't_post'
        db_table_comment = '블로그 게시글'

    def __str__(self):
        return self.title