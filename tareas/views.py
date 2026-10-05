from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, FormView, ListView, UpdateView
from django.views.generic.edit import FormMixin

from .forms import RegistroForm, TareaForm
from .models import Tarea


class RegistroView(FormView):
    """Registra una cuenta e inicia su sesión automáticamente."""

    template_name = "registration/registro.html"
    form_class = RegistroForm
    success_url = reverse_lazy("tareas:lista")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("tareas:lista")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        usuario = form.save()
        login(self.request, usuario)
        messages.success(self.request, f"¡Bienvenido, {usuario.first_name}!")
        return super().form_valid(form)


class TareaListView(LoginRequiredMixin, FormMixin, ListView):
    """Lista las tareas y procesa el formulario del modal de creación."""

    model = Tarea
    form_class = TareaForm
    template_name = "tareas/tarea_list.html"
    context_object_name = "tareas"
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        busqueda = self.request.GET.get("q", "").strip()
        estado = self.request.GET.get("estado", "")
        prioridad = self.request.GET.get("prioridad", "")

        if busqueda:
            queryset = queryset.filter(
                Q(titulo__icontains=busqueda)
                | Q(descripcion__icontains=busqueda)
                | Q(responsable__icontains=busqueda)
            )
        if estado:
            queryset = queryset.filter(estado=estado)
        if prioridad:
            queryset = queryset.filter(prioridad=prioridad)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todas = Tarea.objects.all()
        context.update(
            {
                "total_tareas": todas.count(),
                "tareas_pendientes": todas.filter(estado=Tarea.Estado.PENDIENTE).count(),
                "tareas_en_proceso": todas.filter(estado=Tarea.Estado.EN_PROCESO).count(),
                "tareas_completadas": todas.filter(estado=Tarea.Estado.COMPLETADA).count(),
                "estados": Tarea.Estado.choices,
                "prioridades": Tarea.Prioridad.choices,
                "filtros": self.request.GET,
                "abrir_modal": (
                    self.request.path == reverse("tareas:crear")
                    or self.request.GET.get("nueva") == "1"
                    or bool(context["form"].errors)
                ),
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(request, "La tarea se creó correctamente.")
            return redirect("tareas:lista")
        return self.render_to_response(self.get_context_data(form=form))


class TareaDetailView(LoginRequiredMixin, DetailView):
    model = Tarea
    template_name = "tareas/tarea_detail.html"
    context_object_name = "tarea"


class TareaUpdateView(LoginRequiredMixin, UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = "tareas/tarea_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Los cambios se guardaron correctamente.")
        return super().form_valid(form)


class TareaDeleteView(LoginRequiredMixin, DeleteView):
    model = Tarea
    template_name = "tareas/tarea_confirm_delete.html"
    context_object_name = "tarea"
    success_url = reverse_lazy("tareas:lista")

    def form_valid(self, form):
        messages.success(self.request, "La tarea se eliminó correctamente.")
        return super().form_valid(form)
