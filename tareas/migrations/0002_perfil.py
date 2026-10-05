from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def crear_perfiles_existentes(apps, schema_editor):
    Usuario = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    Perfil = apps.get_model("tareas", "Perfil")
    for usuario in Usuario.objects.all():
        Perfil.objects.get_or_create(usuario_id=usuario.pk)


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tareas", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Perfil",
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
                ("foto", models.FileField(blank=True, upload_to="perfiles/")),
                (
                    "usuario",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="perfil",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"verbose_name": "perfil", "verbose_name_plural": "perfiles"},
        ),
        migrations.RunPython(crear_perfiles_existentes, migrations.RunPython.noop),
    ]
