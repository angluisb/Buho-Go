from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'usuarios'

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('perfil/', login_required(views.perfil), name='perfil'),
]