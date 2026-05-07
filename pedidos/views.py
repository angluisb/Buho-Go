from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, UpdateView
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Pedido, ItemPedido
from .forms import PedidoForm, EstadoPedidoForm
from establecimientos.models import Establecimiento, Producto

class MisPedidosView(ListView):
    """Vista para ver todos los pedidos"""
    model = Pedido
    template_name = 'pedidos/mis_pedidos.html'
    context_object_name = 'pedidos'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Pedido.objects.filter(
                models.Q(usuario=self.request.user) |
                models.Q(cliente_email=self.request.user.email)
            ).order_by('-creado_en')
        else:
            # Para usuarios no autenticados, mostrar pedidos recientes (últimos 50)
            return Pedido.objects.all().order_by('-creado_en')[:50]
    """Vista para ver todos los pedidos"""
    model = Pedido
    template_name = 'pedidos/mis_pedidos.html'
    context_object_name = 'pedidos'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Pedido.objects.filter(
                models.Q(usuario=self.request.user) |
                models.Q(cliente_email=self.request.user.email)
            ).order_by('-creado_en')
        else:
            # Para usuarios no autenticados, mostrar pedidos recientes (últimos 50)
            return Pedido.objects.all().order_by('-creado_en')[:50]

class DetallePedidoView(DetailView):
    """Vista para ver detalles de un pedido"""
    model = Pedido
    template_name = 'pedidos/detalle_pedido.html'
    context_object_name = 'pedido'

    def get_queryset(self):
        return Pedido.objects.all()

def crear_pedido(request, establecimiento_id):
    """Vista para crear un nuevo pedido"""
    establecimiento = get_object_or_404(Establecimiento, id=establecimiento_id, activo=True)
    productos = [
        {
            'id': producto['id'],
            'nombre': producto['nombre'],
            'precio': float(producto['precio']),
        }
        for producto in Producto.objects.filter(establecimiento=establecimiento, disponible=True).values('id', 'nombre', 'precio')
    ]

    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST, user=request.user)
        if pedido_form.is_valid():
            pedido = pedido_form.save(commit=False)
            pedido.establecimiento = establecimiento
            if request.user.is_authenticated:
                pedido.usuario = request.user
            pedido.save()

            total = 0
            for key, value in request.POST.items():
                if key.startswith('producto_') and value:
                    index = key.split('_')[1]
                    cantidad_key = f'cantidad_{index}'
                    if cantidad_key in request.POST and request.POST[cantidad_key]:
                        cantidad = int(request.POST[cantidad_key])
                        if cantidad > 0:
                            producto = get_object_or_404(Producto, id=int(value), establecimiento=establecimiento, disponible=True)
                            precio_unitario = producto.precio
                            subtotal = precio_unitario * cantidad
                            ItemPedido.objects.create(
                                pedido=pedido,
                                producto=producto,
                                cantidad=cantidad,
                                precio_unitario=precio_unitario,
                                subtotal=subtotal
                            )
                            total += subtotal

            pedido.precio_total = total
            pedido.save()
            messages.success(request, 'Pedido creado exitosamente.')
            return redirect('pedidos:detalle_pedido', pk=pedido.pk)
    else:
        pedido_form = PedidoForm(user=request.user)

    context = {
        'establecimiento': establecimiento,
        'productos': productos,
        'pedido_form': pedido_form,
    }
    return render(request, 'pedidos/crear_pedido.html', context)

class GestionarPedidosView(ListView):
    """Vista para gestionar pedidos"""
    model = Pedido
    template_name = 'pedidos/gestionar_pedidos.html'
    context_object_name = 'pedidos'
    paginate_by = 20

    def get_queryset(self):
        return Pedido.objects.all().order_by('-creado_en')

class ActualizarEstadoPedidoView(UpdateView):
    """Vista para actualizar el estado de un pedido"""
    model = Pedido
    form_class = EstadoPedidoForm
    template_name = 'pedidos/actualizar_estado.html'
    success_url = '/pedidos/gestionar/'

    def form_valid(self, form):
        messages.success(self.request, f'Estado del pedido actualizado a: {form.instance.get_estado_display()}')
        return super().form_valid(form)

class GestionarPedidosView(LoginRequiredMixin, ListView):
    """Vista para que el personal del establecimiento gestione pedidos"""
    model = Pedido
    template_name = 'pedidos/gestionar_pedidos.html'
    context_object_name = 'pedidos'
    paginate_by = 20

    def get_queryset(self):
        # Asumiendo que el usuario tiene un establecimiento asignado
        # Por ahora, mostrar todos los pedidos. En producción, filtrar por establecimiento del usuario
        return Pedido.objects.all().order_by('-creado_en')

class ActualizarEstadoPedidoView(LoginRequiredMixin, UpdateView):
    """Vista para actualizar el estado de un pedido"""
    model = Pedido
    form_class = EstadoPedidoForm
    template_name = 'pedidos/actualizar_estado.html'
    success_url = '/pedidos/gestionar/'

    def form_valid(self, form):
        messages.success(self.request, f'Estado del pedido actualizado a: {form.instance.get_estado_display()}')
        return super().form_valid(form)
