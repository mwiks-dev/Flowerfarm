# Generated by Django 4.2.4 on 2023-09-12 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greenhouse', '0006_remove_production_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='production',
            name='production_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
