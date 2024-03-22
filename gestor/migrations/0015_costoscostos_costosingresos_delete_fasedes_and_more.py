# Generated by Django 5.0.1 on 2024-03-20 09:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestor", "0014_costos_bloqueo"),
    ]

    operations = [
        migrations.CreateModel(
            name="Costoscostos",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("codigo", models.CharField(max_length=100)),
                ("tipo", models.CharField(max_length=100)),
                ("aliado", models.CharField(max_length=100)),
                ("fecha_planeada", models.DateField()),
                (
                    "costos_p",
                    models.FloatField(
                        default=0.0,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                ("fecha_pago", models.DateField()),
                (
                    "valor_pagado",
                    models.FloatField(
                        default=0.0,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                (
                    "saldo",
                    models.FloatField(
                        default=0.0,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                ("obsevaciones", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Costosingresos",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("codigo", models.CharField(blank=True, max_length=100, null=True)),
                ("tipo", models.CharField(blank=True, max_length=100, null=True)),
                ("fecha_planeada", models.DateField(blank=True, null=True)),
                (
                    "valor_planeado",
                    models.FloatField(
                        blank=True,
                        default=0.0,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                ("fechapago", models.DateField(blank=True, null=True)),
                (
                    "valorpagado",
                    models.FloatField(
                        blank=True,
                        default=0.0,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                (
                    "saldo",
                    models.FloatField(
                        blank=True,
                        default=0.0,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                (
                    "observaciones",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="FaseDes",
        ),
        migrations.DeleteModel(
            name="SubFaseDes",
        ),
    ]
