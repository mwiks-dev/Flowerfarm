# Generated by Django 4.2.4 on 2023-09-09 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('greenhouse', '0003_alter_user_options_remove_production_staff_number_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='production',
            old_name='staff',
            new_name='staff_member',
        ),
    ]