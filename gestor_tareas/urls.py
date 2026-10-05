"""Rutas principales del proyecto."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

from tareas.forms import CorreoAuthenticationForm
from tareas.views import RegistroView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "acceso/",
        LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=CorreoAuthenticationForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("salir/", LogoutView.as_view(), name="logout"),
    path("registro/", RegistroView.as_view(), name="registro"),
    path("", include("tareas.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Administración de TigTask"
admin.site.site_title = "TigTask"
admin.site.index_title = "Panel administrativo"
