# Generated by Django 5.0.1 on 2024-03-19 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestor", "0011_alter_proyecto_tipo_remove_proyecto_user_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="documentos",
            name="descriocion",
        ),
        migrations.RemoveField(
            model_name="documentos",
            name="link",
        ),
        migrations.RemoveField(
            model_name="documentos",
            name="titulo",
        ),
        migrations.AddField(
            model_name="documentos",
            name="acta_entrega_cliente",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="acta_inicio",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="acta_inicio_aliado",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="acta_recibido_aliado",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="actas_reuniones_tecnicas",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="backlog_oc",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="conciliaciones_proveedor",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="constitucion_proyecto",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="contrato_aliado",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="contrato_cliente",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="correos_clientes_proveedor",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="cronograma",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="entrega_aseguramiento",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="entregas_obligaciones_contractura",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="ficha_cierre",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="ficha_presentacion_proyecto",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="kickoff_cliente_interno",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="matriz_interesados",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="matriz_riesgos",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="obligaciones_contractuales",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="oferta_entregada_cliente",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="plan_gestion_proyecto",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="resumen_oc",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="documentos",
            name="solicitud_control_cambio",
            field=models.BooleanField(default=False),
        ),
    ]