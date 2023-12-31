# Generated by Django 4.2.4 on 2023-09-21 02:00

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greenhouse', '0005_profile_first_time_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default='0701010101', max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='prof_photo',
            field=cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/mwikali/image/upload/v1695192612/icons8-user-90_pt1zqi.png', max_length=255, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='user',
            name='staff_number',
            field=models.IntegerField(null=True, unique=True),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
