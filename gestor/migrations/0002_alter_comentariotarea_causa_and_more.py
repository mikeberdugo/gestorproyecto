# Generated by Django 5.0.1 on 2024-03-14 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestor", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comentariotarea",
            name="causa",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="comentariotarea",
            name="identificando_problema",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="comentariotarea",
            name="planes_mejora_aplicados",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="comentariotarea",
            name="resultados_planes_mejora",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="comentariotarea",
            name="solucion",
            field=models.TextField(blank=True, null=True),
        ),
    ]
