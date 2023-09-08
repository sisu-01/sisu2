from django.db import models

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