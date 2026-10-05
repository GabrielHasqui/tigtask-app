from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Perfil


@receiver(post_save, sender=get_user_model())
def crear_perfil_de_usuario(sender, instance, created, **kwargs):
    """Garantiza que cada usuario nuevo tenga un perfil asociado."""

    if created:
        Perfil.objects.create(usuario=instance)
