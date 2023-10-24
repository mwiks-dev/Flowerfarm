# Generated by Django 4.2.4 on 2023-10-24 05:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('greenhouse', '0014_rename_varieties_production_new_varieties'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='production',
            name='new_varieties',
        ),
        migrations.AddField(
            model_name='production',
            name='new_varieties',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='greenhouse.variety'),
        ),
    ]