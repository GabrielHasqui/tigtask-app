from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Tarea


class CorreoAuthenticationForm(AuthenticationForm):
    """Formulario de acceso que presenta el usuario como correo electrónico."""

    username = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(
            attrs={
                "autofocus": True,
                "autocomplete": "email",
                "placeholder": "nombre@correo.com",
            }
        ),
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "Ingresa tu contraseña",
            }
        ),
    )


class RegistroForm(UserCreationForm):
    """Crea usuarios usando el correo como identificador de acceso."""

    first_name = forms.CharField(
        label="Nombres",
        max_length=150,
        widget=forms.TextInput(
            attrs={"autocomplete": "given-name", "placeholder": "Tus nombres"}
        ),
    )
    last_name = forms.CharField(
        label="Apellidos",
        max_length=150,
        widget=forms.TextInput(
            attrs={"autocomplete": "family-name", "placeholder": "Tus apellidos"}
        ),
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "placeholder": "nombre@correo.com"}
        ),
    )
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "placeholder": "Crea una contraseña"}
        ),
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "placeholder": "Repite la contraseña"}
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if get_user_model().objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = " ".join(self.cleaned_data["first_name"].split()).title()
        user.last_name = " ".join(self.cleaned_data["last_name"].split()).title()
        user.email = self.cleaned_data["email"]
        user.username = user.email
        if commit:
            user.save()
        return user


class TareaForm(forms.ModelForm):
    """Formulario único para crear y editar tareas."""

    class Meta:
        model = Tarea
        fields = [
            "titulo",
            "descripcion",
            "responsable",
            "prioridad",
            "estado",
            "fecha_limite",
        ]
        widgets = {
            "titulo": forms.TextInput(
                attrs={"placeholder": "Ej. Corregir formulario de acceso"}
            ),
            "descripcion": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Describe brevemente el trabajo a realizar"}
            ),
            "responsable": forms.TextInput(
                attrs={"placeholder": "Nombre de la persona responsable"}
            ),
            "fecha_limite": forms.DateInput(attrs={"type": "date"}),
        }
        help_texts = {
            "fecha_limite": "Este campo es opcional.",
        }
