# Generated by Django 5.0 on 2024-03-08 01:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablero',
            name='proyect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tablero', to='gestor.proyecto'),
        ),
    ]