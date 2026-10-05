from django.urls import path

from .views import (
    TareaDeleteView,
    TareaDetailView,
    TareaListView,
    TareaUpdateView,
)

app_name = "tareas"

urlpatterns = [
    path("", TareaListView.as_view(), name="lista"),
    path("tareas/nueva/", TareaListView.as_view(), name="crear"),
    path("tareas/<int:pk>/", TareaDetailView.as_view(), name="detalle"),
    path("tareas/<int:pk>/editar/", TareaUpdateView.as_view(), name="editar"),
    path("tareas/<int:pk>/eliminar/", TareaDeleteView.as_view(), name="eliminar"),
]
