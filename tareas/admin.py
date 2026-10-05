from django.contrib import admin

from .models import Perfil, Tarea


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("usuario", "foto")
    search_fields = ("usuario__username", "usuario__first_name", "usuario__last_name")


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "responsable", "prioridad", "estado", "fecha_limite")
    list_filter = ("estado", "prioridad")
    search_fields = ("titulo", "descripcion", "responsable")
    ordering = ("-fecha_creacion",)
