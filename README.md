# 🦉 Buho Go — Plataforma de Pedidos Universitarios

Plataforma para que estudiantes de la Universidad de Sonora realicen pedidos anticipados en comercios cercanos al campus.

## Equipo

- Luis Angel Bracamonte Murillo
- Carlos Eduardo Fierros Sesma
- Arturo Cordova
- Orlando Bojórquez

## Tecnologías

- **Backend:** Django 4.2
- **Base de datos:** SQLite (desarrollo) / MySQL (producción)
- **Frontend:** HTML + Bootstrap 5

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/buho-go.git
cd buho-go

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Edita .env con tu SECRET_KEY

# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear superusuario (admin)
python manage.py createsuperuser

# 7. Correr servidor
python manage.py runserver
```

## Funcionalidades implementadas (Sprint 1 y 2)

- ✅ Registro de usuario
- ✅ Inicio de sesión
- ✅ Ver catálogo de establecimientos
- ✅ Ver productos por establecimiento
- ✅ Realizar pedido anticipado
- ✅ Ver estado de mis pedidos
- ⚙️ Notificaciones (pendiente)

## Metodología

Proyecto desarrollado con **Scrum**. Ver tablero en Trello.
