from django.apps import AppConfig


class TareasConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tareas"
    verbose_name = "Gestión de tareas"

    def ready(self):
        from . import signals  # noqa: F401
