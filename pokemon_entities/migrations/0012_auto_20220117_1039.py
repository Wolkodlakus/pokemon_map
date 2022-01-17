# Generated by Django 3.1.14 on 2022-01-17 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0011_auto_20220117_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonentity',
            name='pokemon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon_entities', to='pokemon_entities.pokemon', verbose_name='Размещаемый покемон'),
        ),
    ]
