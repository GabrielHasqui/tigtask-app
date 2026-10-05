from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Tarea


class TareaModelTests(TestCase):
    def test_el_nombre_de_la_tarea_es_su_titulo(self):
        tarea = Tarea(titulo="Preparar versión 1.0")
        self.assertEqual(str(tarea), "Preparar versión 1.0")


class TareaViewTests(TestCase):
    def setUp(self):
        self.usuario = get_user_model().objects.create_user(
            username="pruebas@unemi.edu.ec",
            email="pruebas@unemi.edu.ec",
            password="ClavePruebas12..",
        )
        self.client.force_login(self.usuario)
        self.tarea = Tarea.objects.create(
            titulo="Corregir formulario",
            descripcion="Validar los campos obligatorios.",
            responsable="Ana",
            prioridad=Tarea.Prioridad.ALTA,
            fecha_limite=date(2030, 1, 20),
        )

    def test_lista_muestra_las_tareas(self):
        response = self.client.get(reverse("tareas:lista"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corregir formulario")

    def test_filtro_por_estado(self):
        response = self.client.get(reverse("tareas:lista"), {"estado": "completada"})
        self.assertNotIn(self.tarea, response.context["tareas"])

    def test_crear_tarea(self):
        response = self.client.post(
            reverse("tareas:crear"),
            {
                "titulo": "Actualizar documentación",
                "descripcion": "Completar el archivo README.",
                "responsable": "Luis",
                "prioridad": "media",
                "estado": "pendiente",
                "fecha_limite": "2030-02-10",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tarea.objects.filter(titulo="Actualizar documentación").exists())

    def test_ruta_de_creacion_abre_el_modal(self):
        response = self.client.get(reverse("tareas:crear"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["abrir_modal"])
        self.assertContains(response, 'id="task-modal"')

    def test_modal_muestra_errores_de_validacion(self):
        response = self.client.post(reverse("tareas:crear"), {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertContains(response, 'data-auto-open="true"')

    def test_editar_tarea(self):
        response = self.client.post(
            reverse("tareas:editar", args=[self.tarea.pk]),
            {
                "titulo": "Formulario corregido",
                "descripcion": self.tarea.descripcion,
                "responsable": self.tarea.responsable,
                "prioridad": "alta",
                "estado": "completada",
                "fecha_limite": "2030-01-20",
            },
        )
        self.tarea.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.tarea.estado, Tarea.Estado.COMPLETADA)

    def test_eliminar_tarea(self):
        response = self.client.post(reverse("tareas:eliminar", args=[self.tarea.pk]))
        self.assertRedirects(response, reverse("tareas:lista"))
        self.assertFalse(Tarea.objects.filter(pk=self.tarea.pk).exists())


class AccesoTests(TestCase):
    def setUp(self):
        self.correo = "usuario@unemi.edu.ec"
        self.clave = "ClaveSegura12.."
        get_user_model().objects.create_user(
            username=self.correo,
            email=self.correo,
            first_name="Usuario",
            last_name="De Prueba",
            password=self.clave,
        )

    def test_lista_requiere_iniciar_sesion(self):
        response = self.client.get(reverse("tareas:lista"))
        self.assertRedirects(response, f"{reverse('login')}?next=/")

    def test_usuario_puede_acceder_con_su_correo(self):
        response = self.client.post(
            reverse("login"),
            {"username": self.correo, "password": self.clave},
        )
        self.assertRedirects(response, reverse("tareas:lista"))

    def test_nav_muestra_el_primer_nombre_y_apellido(self):
        self.client.login(username=self.correo, password=self.clave)
        response = self.client.get(reverse("tareas:lista"))
        self.assertContains(response, "Usuario De")
        self.assertContains(response, "tigtask-avatar-default.png")

    def test_usuario_nuevo_recibe_un_perfil(self):
        usuario = get_user_model().objects.create_user(
            username="perfil@unemi.edu.ec",
            email="perfil@unemi.edu.ec",
            password="ClavePerfil12..",
        )
        self.assertIsNotNone(usuario.perfil)

    def test_registro_crea_usuario_e_inicia_sesion(self):
        response = self.client.post(
            reverse("registro"),
            {
                "first_name": "María Elena",
                "last_name": "López Ruiz",
                "email": "maria@unemi.edu.ec",
                "password1": "ClaveRegistro12..",
                "password2": "ClaveRegistro12..",
            },
        )
        self.assertRedirects(response, reverse("tareas:lista"))
        usuario = get_user_model().objects.get(email="maria@unemi.edu.ec")
        self.assertEqual(usuario.get_full_name(), "María Elena López Ruiz")
        self.assertEqual(int(self.client.session["_auth_user_id"]), usuario.pk)
