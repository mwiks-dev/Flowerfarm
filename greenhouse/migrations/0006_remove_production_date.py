# Generated by Django 4.2.4 on 2023-09-11 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('greenhouse', '0005_production_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='production',
            name='date',
        ),
    ]
