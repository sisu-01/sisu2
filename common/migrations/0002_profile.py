# Generated by Django 4.2.4 on 2023-10-30 06:45

import common.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=10)),
                ('desc', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to=common.utils.ImageUpload('poster'))),
            ],
            options={
                'db_table': 'profile',
                'db_table_comment': '소개',
                'managed': True,
            },
        ),
    ]