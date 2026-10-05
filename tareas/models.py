from django.db import models
from django.conf import settings
from django.urls import reverse


class Perfil(models.Model):
    """Datos visuales opcionales asociados a cada usuario."""

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    foto = models.FileField(upload_to="perfiles/", blank=True)

    class Meta:
        verbose_name = "perfil"
        verbose_name_plural = "perfiles"

    def __str__(self):
        return f"Perfil de {self.usuario.username}"


class Tarea(models.Model):
    """Representa una actividad sencilla dentro de un proyecto de software."""

    class Prioridad(models.TextChoices):
        BAJA = "baja", "Baja"
        MEDIA = "media", "Media"
        ALTA = "alta", "Alta"

    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        EN_PROCESO = "en_proceso", "En proceso"
        COMPLETADA = "completada", "Completada"

    titulo = models.CharField("título", max_length=120)
    descripcion = models.TextField("descripción")
    responsable = models.CharField(max_length=100)
    prioridad = models.CharField(
        max_length=10,
        choices=Prioridad.choices,
        default=Prioridad.MEDIA,
    )
    estado = models.CharField(
        max_length=12,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )
    fecha_limite = models.DateField("fecha límite", blank=True, null=True)
    fecha_creacion = models.DateTimeField("fecha de creación", auto_now_add=True)
    fecha_actualizacion = models.DateTimeField("última actualización", auto_now=True)

    class Meta:
        ordering = ["-fecha_creacion"]
        verbose_name = "tarea"
        verbose_name_plural = "tareas"

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("tareas:detalle", kwargs={"pk": self.pk})
