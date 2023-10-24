# Generated by Django 4.2.4 on 2023-10-24 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greenhouse', '0020_alter_production_varieties'),
    ]

    operations = [
        migrations.AlterField(
            model_name='production',
            name='varieties',
            field=models.CharField(choices=[('Athena', 'Athena'), ('Belle Rose', 'Belle Rose'), ('Confidential', 'Confidential'), ('Espana', 'Espana'), ('Esperance', 'Esperance'), ('Ever Red', 'Ever Red'), ('Fire Expressions', 'Fire Expressions'), ('Fuschiana', 'Fuschiana'), ('Golden Finch', 'Golden Finch'), ('Good times', 'Good times'), ('Jumilia', 'Jumilia'), ('Madam Cerise', 'Madam Cerise'), ('Madam Pink', 'Madam Pink'), ('Madam Red', 'Madam Red'), ('Magic Avalanche+', 'Magic Avalanche+'), ('Mandala', 'Mandala'), ('Miss Mardi', 'Miss Mardi'), ('Moonwalk', 'Moonwalk'), ('New Orleans', 'New Orleans'), ('Novavita', 'Novavita'), ('Opala', 'Opala'), ('Revival', 'Revival'), ('Tacazzi+', 'Tacazzi+'), ('Tara', 'Tara'), ('Wham', 'Wham'), ('Yellowing', 'Yellowing')], default='Athena', max_length=50),
        ),
        migrations.DeleteModel(
            name='Variety',
        ),
    ]