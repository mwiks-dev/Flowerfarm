# Generated by Django 4.2.4 on 2023-09-19 22:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('greenhouse', '0003_alter_user_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='production',
            name='staff_member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
