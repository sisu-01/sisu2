from django.db import models

# Create your models here.
class BlogTree(models.Model):
    title = models.CharField(max_length=20)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='tree', null=True, blank=True)
    seq = models.IntegerField()

    class Meta:
        managed = True
        db_table = 't_blog_tree'
        db_table_comment = '블로그 트리 메뉴'

    def __str__(self):
            return self.title
    
class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    thumbnail = models.CharField(max_length=100, null=True)
    is_public = models.BooleanField()
    insert_date = models.DateTimeField()
    insert_ip = models.CharField(max_length=40)
    update_date = models.DateTimeField(blank=True, null=True)
    update_ip = models.CharField(max_length=40, blank=True, null=True)
    tree = models.ForeignKey(BlogTree, on_delete=models.SET_NULL, related_name='post', null=True)
    view_count = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 't_blog_post'
        db_table_comment = '블로그 게시글'

    def __str__(self):
        return self.title
    
class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comment')
    is_authenticated = models.BooleanField()
    nickname = models.CharField(max_length=12)
    password = models.CharField(max_length=128)
    content = models.CharField(max_length=400)
    insert_date = models.DateTimeField()
    insert_ip = models.CharField(max_length=40)

    class Meta:
        managed = True
        db_table = 't_blog_comment'
        db_table_comment = '블로그 댓글'

    def __str__(self):
        return self.post