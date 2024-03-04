# Generated by Django 5.0 on 2024-03-03 16:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matrizriesgo',
            name='gravedad',
            field=models.CharField(choices=[('Bajo2', 'Muy Bajo'), ('medio', 'Medio'), ('alto2', 'Muy Alto'), ('alto1', 'Alto'), ('bajo1', 'Bajo')], max_length=20),
        ),
        migrations.AlterField(
            model_name='matrizriesgo',
            name='probavilidad',
            field=models.CharField(choices=[('Bajo2', 'Muy Bajo'), ('medio', 'Medio'), ('alto2', 'Muy Alto'), ('alto1', 'Alto'), ('bajo1', 'Bajo')], max_length=20),
        ),
        migrations.AlterField(
            model_name='tablero',
            name='proyect',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tablero', to='gestor.proyecto'),
        ),
    ]
