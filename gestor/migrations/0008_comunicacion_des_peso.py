# Generated by Django 5.0.1 on 2024-03-15 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestor", "0007_remove_proyecto_grupo_proyecto_grupo"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comunicacion",
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
                ("rol", models.CharField(max_length=100)),
                ("nombre", models.CharField(max_length=100)),
                ("celular", models.CharField(max_length=20)),
                ("correo", models.EmailField(max_length=254)),
                ("aspectos_a_comunicar", models.TextField()),
                ("responsable_de_la_comunicacion", models.TextField()),
                ("cuando_lo_comunica", models.TextField()),
                ("importancia", models.TextField()),
                ("estrategias_y_medios", models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name="des",
            name="peso",
            field=models.IntegerField(
                blank=True, default=1, verbose_name="Peso de actividad"
            ),
        ),
    ]
