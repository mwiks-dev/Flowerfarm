# Generated by Django 4.2.4 on 2023-10-19 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('greenhouse', '0013_remove_production_variety_production_varieties'),
    ]

    operations = [
        migrations.RenameField(
            model_name='production',
            old_name='varieties',
            new_name='new_varieties',
        ),
    ]
