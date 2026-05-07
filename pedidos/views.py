from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Pedido, ItemPedido
from .forms import PedidoForm, ItemPedidoForm, EstadoPedidoForm
from establecimientos.models import Establecimiento, Producto


# ========== HELPERS PARA CARRITO ==========
def _get_carrito(request):
    """Obtiene el carrito de la sesión"""
    return request.session.get('carrito', {'establecimiento': None, 'items': {}})


def _save_carrito(request, carrito):
    """Guarda el carrito en la sesión"""
    request.session['carrito'] = carrito
    request.session.modified = True


def _carrito_items(request, establecimiento):
    """Retorna los items del carrito y el total para un establecimiento específico"""
    carrito = _get_carrito(request)
    
    # Verificar que el carrito sea para este establecimiento
    if not carrito.get('establecimiento') or int(carrito.get('establecimiento')) != establecimiento.id:
        return [], 0

    items_data = carrito.get('items', {})
    producto_ids = [int(pid) for pid, qty in items_data.items() if qty and int(qty) > 0]
    
    if not producto_ids:
        return [], 0
    
    productos = Producto.objects.filter(
        id__in=producto_ids,
        establecimiento=establecimiento,
        disponible=True
    )

    items = []
    total = 0
    for producto in productos:
        cantidad = int(items_data.get(str(producto.id), 0))
        if cantidad <= 0:
            continue
        subtotal = producto.precio * cantidad
        total += subtotal
        items.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })

    return items, total


# ========== OPERACIONES DEL CARRITO ==========
@login_required
def agregar_al_carrito(request):
    """Agrega un producto al carrito"""
    if request.method != 'POST':
        return redirect('establecimientos:lista_establecimientos')
    
    producto_id = request.POST.get('producto_id')
    establecimiento_id = request.POST.get('establecimiento_id')
    cantidad = int(request.POST.get('cantidad', 1))
    
    if cantidad < 1:
        cantidad = 1
    
    establecimiento = get_object_or_404(Establecimiento, id=establecimiento_id, activo=True)
    producto = get_object_or_404(Producto, id=producto_id, establecimiento=establecimiento, disponible=True)
    
    carrito = _get_carrito(request)
    
    # Si el carrito es de otro establecimiento, limpiarlo
    if carrito.get('establecimiento') and int(carrito.get('establecimiento')) != establecimiento.id:
        carrito = {'establecimiento': establecimiento.id, 'items': {}}
    
    # Inicializar items si no existen
    if not carrito.get('items'):
        carrito['items'] = {}
    
    carrito['establecimiento'] = establecimiento.id
    
    # Agregar o actualizar cantidad
    producto_key = str(producto.id)
    carrito['items'][producto_key] = carrito['items'].get(producto_key, 0) + cantidad
    
    _save_carrito(request, carrito)
    
    messages.success(request, f'{producto.nombre} agregado al carrito.')
    return redirect('establecimientos:detalle_establecimiento', pk=establecimiento.id)


@login_required
def eliminar_producto_carrito(request, producto_id):
    """Elimina un producto del carrito"""
    carrito = _get_carrito(request)
    
    if str(producto_id) in carrito.get('items', {}):
        del carrito['items'][str(producto_id)]
        _save_carrito(request, carrito)
        messages.info(request, 'Producto removido del carrito.')
    
    establecimiento_id = carrito.get('establecimiento')
    if establecimiento_id:
        return redirect('establecimientos:detalle_establecimiento', pk=establecimiento_id)
    
    return redirect('establecimientos:lista_establecimientos')


@login_required
def limpiar_carrito(request):
    """Limpia todo el carrito"""
    request.session.pop('carrito', None)
    request.session.modified = True
    messages.info(request, 'Carrito vaciado.')
    return redirect('establecimientos:lista_establecimientos')


# ========== VISTAS PRINCIPALES ==========
class MisPedidosView(LoginRequiredMixin, ListView):
    """Vista para que los usuarios vean sus pedidos"""
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
    """Vista para crear un nuevo pedido desde el carrito"""
    establecimiento = get_object_or_404(Establecimiento, id=establecimiento_id, activo=True)
    
    carrito = _get_carrito(request)
    carrito_items, carrito_total = _carrito_items(request, establecimiento)
    
    # Verificar que hay items en el carrito
    if not carrito_items:
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('establecimientos:detalle_establecimiento', pk=establecimiento.id)

    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST)
        if pedido_form.is_valid():
            pedido = pedido_form.save(commit=False)
            pedido.usuario = request.user
            pedido.establecimiento = establecimiento
            pedido.save()

            # Crear items del pedido desde el carrito
            total = 0
            for item in carrito_items:
                producto = item['producto']
                cantidad = item['cantidad']
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
            
            # Limpiar carrito
            request.session.pop('carrito', None)
            request.session.modified = True
            
            messages.success(request, 'Pedido creado exitosamente.')
            return redirect('pedidos:detalle_pedido', pk=pedido.pk)
    else:
        pedido_form = PedidoForm()

    context = {
        'establecimiento': establecimiento,
        'carrito_items': carrito_items,
        'carrito_total': carrito_total,
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
        # Mostrar todos los pedidos
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
