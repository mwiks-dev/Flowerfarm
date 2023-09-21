# Generated by Django 4.2.4 on 2023-09-21 02:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('greenhouse', '0007_alter_production_staff_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='production',
            name='staff_member',
        ),
        migrations.AddField(
            model_name='production',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
