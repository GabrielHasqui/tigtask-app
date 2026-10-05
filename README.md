# TigTask - Sistema de Gestión de Tareas

TigTask es una aplicación web sencilla desarrollada con Django para administrar las tareas de un equipo de software. El proyecto permite aplicar control de versiones, seguimiento de cambios y organización de elementos de configuración durante una práctica experimental.

## Funciones

- Crear, consultar, editar y eliminar tareas.
- Clasificar por prioridad y estado.
- Buscar por título, descripción o responsable.
- Filtrar las tareas desde el listado.
- Consultar un resumen del avance del proyecto.
- Registrar usuarios e iniciar sesión mediante correo electrónico.
- Mostrar el nombre y la imagen de perfil del usuario.
- Administrar los registros desde Django Admin.

## Tecnologías

- Python 3.12
- Django 5.2
- SQLite
- HTML y CSS responsive
- Lucide Icons

## Instalación

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abrir `http://127.0.0.1:8000/` en el navegador.

La base de datos local, los archivos cargados y el entorno virtual están excluidos del repositorio. Cada instalación comienza con datos independientes.

## Pruebas

```powershell
python manage.py test
```

## Panel administrativo

Crear un usuario administrador:

```powershell
python manage.py createsuperuser
```

Después, abrir `http://127.0.0.1:8000/admin/`.

## Política sencilla de ramas y commits

- `main`: versión estable.
- `develop`: integración de cambios.
- `feature/nombre`: nuevas funciones.
- `fix/nombre`: corrección de errores.

Formato sugerido para los commits:

```text
tipo: descripción breve
```

Ejemplos: `feat: agregar filtro por prioridad` y `fix: corregir edición de tareas`.

## Versión

Versión actual: **1.0.0**. Los cambios se detallan en `CHANGELOG.md`.
