from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView
from .models import Establecimiento, Producto
from .forms import EstablecimientoForm, ProductoForm


def _get_carrito(request):
    """Obtiene el carrito de la sesión"""
    return request.session.get('carrito', {'establecimiento': None, 'items': {}})


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


def home(request):
    """Vista principal - lista establecimientos y productos destacados"""
    establecimientos = Establecimiento.objects.filter(activo=True)[:6]
    productos = Producto.objects.filter(disponible=True)[:8]

    return render(request, 'home.html', {
        'establecimientos': establecimientos,
        'productos': productos
    })


class ListaEstablecimientosView(ListView):
    """Lista todos los establecimientos activos"""
    model = Establecimiento
    template_name = 'establecimientos/lista_establecimientos.html'
    context_object_name = 'establecimientos'
    paginate_by = 12

    def get_queryset(self):
        return Establecimiento.objects.filter(activo=True)


class ComercioRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.tipo == 'comercio'

    def handle_no_permission(self):
        return redirect('home')


class MisEstablecimientosView(ComercioRequiredMixin, ListView):
    """Lista los establecimientos del comercio que inició sesión"""
    model = Establecimiento
    template_name = 'establecimientos/mis_establecimientos.html'
    context_object_name = 'establecimientos'
    paginate_by = 12

    def get_queryset(self):
        return Establecimiento.objects.filter(propietario=self.request.user)


class CrearEstablecimientoView(ComercioRequiredMixin, CreateView):
    model = Establecimiento
    form_class = EstablecimientoForm
    template_name = 'establecimientos/crear_establecimiento.html'
    success_url = reverse_lazy('establecimientos:mis_establecimientos')

    def form_valid(self, form):
        form.instance.propietario = self.request.user
        return super().form_valid(form)


class CrearProductoView(ComercioRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'establecimientos/crear_producto.html'

    def dispatch(self, request, *args, **kwargs):
        self.establecimiento = get_object_or_404(
            Establecimiento,
            pk=kwargs['establecimiento_id'],
            propietario=request.user
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.establecimiento = self.establecimiento
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['establecimiento'] = self.establecimiento
        return context

    def get_success_url(self):
        return reverse_lazy('establecimientos:detalle_establecimiento', kwargs={'pk': self.establecimiento.pk})


class DetalleEstablecimientoView(DetailView):
    """Detalle de un establecimiento con productos y carrito"""
    model = Establecimiento
    template_name = 'establecimientos/detalle_establecimiento.html'
    context_object_name = 'establecimiento'

    def get_queryset(self):
        return Establecimiento.objects.filter(activo=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        establecimiento = self.get_object()
        
        # Obtener productos disponibles
        context['productos'] = Producto.objects.filter(
            establecimiento=establecimiento,
            disponible=True
        )
        
        # Obtener items del carrito para este establecimiento
        carrito_items, carrito_total = _carrito_items(self.request, establecimiento)
        context['carrito_items'] = carrito_items
        context['carrito_total'] = carrito_total
        
        return context