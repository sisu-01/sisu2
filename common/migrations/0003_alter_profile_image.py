# Generated by Django 4.2.4 on 2023-10-30 06:55

import common.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(upload_to=common.utils.ImageUpload('profile')),
        ),
    ]
