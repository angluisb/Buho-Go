from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegistroForm, LoginForm
from django.contrib.auth.decorators import login_required
# Create your views here.


def registro(request):
    if request.user.is_authenticated:
        return redirect('establecimientos:lista_establecimientos')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f'¡Bienvenido {usuario.first_name}! Tu cuenta fue creada.')
            return redirect('establecimientos:lista_establecimientos')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form})


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect('establecimientos:lista_establecimientos')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            messages.success(request, f'¡Hola de nuevo, {usuario.first_name or usuario.username}!')
            return redirect('establecimientos:lista_establecimientos')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'usuarios/login.html', {'form': form})


def cerrar_sesion(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('usuarios:login')


@login_required
def perfil(request):
    """Vista del perfil del usuario autenticado."""
    return render(request, 'usuarios/perfil.html')