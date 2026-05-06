from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Pedido, ItemPedido
from .forms import PedidoForm, ItemPedidoForm, EstadoPedidoForm
from establecimientos.models import Establecimiento, Producto

class MisPedidosView(LoginRequiredMixin, ListView):
    """Vista para que los estudiantes vean sus pedidos"""
    model = Pedido
    template_name = 'pedidos/mis_pedidos.html'
    context_object_name = 'pedidos'
    paginate_by = 10

    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user).order_by('-creado_en')

class DetallePedidoView(LoginRequiredMixin, DetailView):
    """Vista para ver detalles de un pedido"""
    model = Pedido
    template_name = 'pedidos/detalle_pedido.html'
    context_object_name = 'pedido'

    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user)

@login_required
def crear_pedido(request, establecimiento_id):
    """Vista para crear un nuevo pedido"""
    establecimiento = get_object_or_404(Establecimiento, id=establecimiento_id, activo=True)
    productos = Producto.objects.filter(establecimiento=establecimiento, disponible=True)

    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST)
        if pedido_form.is_valid():
            pedido = pedido_form.save(commit=False)
            pedido.usuario = request.user
            pedido.establecimiento = establecimiento
            pedido.save()

            # Procesar items del pedido desde el formulario dinámico
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
            return redirect('detalle_pedido', pk=pedido.pk)
    else:
        pedido_form = PedidoForm()

    context = {
        'establecimiento': establecimiento,
        'productos': productos,
        'pedido_form': pedido_form,
    }
    return render(request, 'pedidos/crear_pedido.html', context)

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
