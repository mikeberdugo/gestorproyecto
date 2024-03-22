# Generated by Django 5.0.1 on 2024-03-19 14:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "gestor",
            "0012_remove_documentos_descriocion_remove_documentos_link_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="costos",
            old_name="aliado",
            new_name="cliente",
        ),
        migrations.RenameField(
            model_name="costos",
            old_name="contrato_aliado",
            new_name="codigo",
        ),
        migrations.RemoveField(
            model_name="costos",
            name="backlog",
        ),
        migrations.RemoveField(
            model_name="costos",
            name="meses",
        ),
        migrations.RemoveField(
            model_name="costos",
            name="objeto",
        ),
        migrations.RemoveField(
            model_name="costos",
            name="one_time",
        ),
        migrations.RemoveField(
            model_name="costos",
            name="proyecto",
        ),
        migrations.RemoveField(
            model_name="costos",
            name="recurrente",
        ),
        migrations.RemoveField(
            model_name="costos",
            name="tipo",
        ),
        migrations.AddField(
            model_name="costos",
            name="costo_presupuestado",
            field=models.FloatField(
                default=0.0, validators=[django.core.validators.MinValueValidator(0.0)]
            ),
        ),
        migrations.AddField(
            model_name="costos",
            name="margen",
            field=models.FloatField(
                default=0.0,
                validators=[
                    django.core.validators.MinValueValidator(0.0),
                    django.core.validators.MaxValueValidator(100.0),
                ],
            ),
        ),
        migrations.AddField(
            model_name="costos",
            name="utilidad",
            field=models.FloatField(
                default=0.0, validators=[django.core.validators.MinValueValidator(0.0)]
            ),
        ),
        migrations.AddField(
            model_name="costos",
            name="valor_total_ingreso",
            field=models.FloatField(
                default=0.0, validators=[django.core.validators.MinValueValidator(0.0)]
            ),
        ),
    ]
