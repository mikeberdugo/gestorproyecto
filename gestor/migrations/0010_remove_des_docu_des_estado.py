# Generated by Django 5.0.1 on 2024-03-15 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestor", "0009_acti"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="des",
            name="docu",
        ),
        migrations.AddField(
            model_name="des",
            name="estado",
            field=models.CharField(blank=True, max_length=200),
        ),
    ]