# Generated by Django 5.0.1 on 2024-03-15 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestor", "0008_comunicacion_des_peso"),
    ]

    operations = [
        migrations.CreateModel(
            name="Acti",
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
                ("fasedes", models.CharField(max_length=200)),
                ("subfasedes", models.CharField(max_length=200)),
                ("tarea", models.CharField(max_length=200)),
                (
                    "horas",
                    models.IntegerField(
                        blank=True, default=0, verbose_name="Tiempo Estimado (horas)"
                    ),
                ),
            ],
        ),
    ]
