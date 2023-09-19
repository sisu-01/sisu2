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
    """
    제목
    내용
    조회수
    썸네일
    추천수
    댓글수
    글쓴이
    작성일
    작성ip
    수정일
    수정ip
    공개,비공개
    메뉴
    """
    class Meta:
        managed = True
        db_table = 't_post'
        db_table_comment = '블로그 게시글'

    def __str__(self):
        return self.title