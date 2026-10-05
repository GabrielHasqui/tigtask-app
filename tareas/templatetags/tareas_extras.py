from django import template

register = template.Library()


@register.filter
def nombre_corto(usuario):
    """Devuelve únicamente el primer nombre y el primer apellido."""

    nombres = usuario.first_name.split()
    apellidos = usuario.last_name.split()
    partes = []
    if nombres:
        partes.append(nombres[0])
    if apellidos:
        partes.append(apellidos[0])
    return " ".join(partes) or usuario.email or usuario.username
