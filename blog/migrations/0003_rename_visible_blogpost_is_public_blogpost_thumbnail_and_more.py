# Generated by Django 4.2.4 on 2023-10-18 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_blogpost_tree'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpost',
            old_name='visible',
            new_name='is_public',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='thumbnail',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='view_count',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
