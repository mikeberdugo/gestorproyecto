# Generated by Django 5.0 on 2024-03-01 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0003_columna_postit_proyecto_columna_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matrizriesgo',
            name='gravedad',
            field=models.CharField(choices=[('alto2', 'Muy Alto'), ('bajo1', 'Bajo'), ('Bajo2', 'Muy Bajo'), ('alto1', 'Alto'), ('medio', 'Medio')], max_length=20),
        ),
        migrations.AlterField(
            model_name='matrizriesgo',
            name='probavilidad',
            field=models.CharField(choices=[('alto2', 'Muy Alto'), ('bajo1', 'Bajo'), ('Bajo2', 'Muy Bajo'), ('alto1', 'Alto'), ('medio', 'Medio')], max_length=20),
        ),
    ]
