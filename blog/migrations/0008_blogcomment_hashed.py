# Generated by Django 4.2.4 on 2023-10-30 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_blogcomment_content_alter_blogcomment_nickname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcomment',
            name='hashed',
            field=models.CharField(max_length=128, null=True),
        ),
    ]