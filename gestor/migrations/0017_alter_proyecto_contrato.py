# Generated by Django 5.0.1 on 2024-03-21 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestor", "0016_proyecto_cliente_proyecto_contrato_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="proyecto",
            name="contrato",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
