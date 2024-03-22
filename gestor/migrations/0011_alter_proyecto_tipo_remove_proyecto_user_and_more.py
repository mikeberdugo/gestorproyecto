# Generated by Django 5.0.1 on 2024-03-16 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestor", "0010_remove_des_docu_des_estado"),
    ]

    operations = [
        migrations.AlterField(
            model_name="proyecto",
            name="tipo",
            field=models.CharField(
                choices=[
                    ("Proyectos Integración", "Proyectos Integración"),
                    ("Necesidades entrega operación", "Necesidades entrega operación"),
                    ("Proyectos Producto Propio", "Necesidades entrega operación"),
                    ("Necesidades", "Necesidades"),
                ],
                max_length=50,
            ),
        ),
        migrations.RemoveField(
            model_name="proyecto",
            name="user",
        ),
        migrations.AddField(
            model_name="proyecto",
            name="user",
            field=models.ManyToManyField(to="gestor.usuario"),
        ),
    ]