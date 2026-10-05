# Generated for the academic task management project.
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tarea",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("titulo", models.CharField(max_length=120, verbose_name="título")),
                ("descripcion", models.TextField(verbose_name="descripción")),
                ("responsable", models.CharField(max_length=100)),
                ("prioridad", models.CharField(choices=[("baja", "Baja"), ("media", "Media"), ("alta", "Alta")], default="media", max_length=10)),
                ("estado", models.CharField(choices=[("pendiente", "Pendiente"), ("en_proceso", "En proceso"), ("completada", "Completada")], default="pendiente", max_length=12)),
                ("fecha_limite", models.DateField(blank=True, null=True, verbose_name="fecha límite")),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")),
                ("fecha_actualizacion", models.DateTimeField(auto_now=True, verbose_name="última actualización")),
            ],
            options={
                "verbose_name": "tarea",
                "verbose_name_plural": "tareas",
                "ordering": ["-fecha_creacion"],
            },
        ),
    ]

