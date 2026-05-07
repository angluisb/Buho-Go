from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Establecimiento, Producto

from django.shortcuts import render
from establecimientos.models import Establecimiento


def home(request):

    establecimientos = Establecimiento.objects.all()[:6]

    productos = Producto.objects.all()[:8]

    return render(request, 'home.html', {
        'establecimientos': establecimientos,
        'productos': productos
    })


def _get_carrito(request):
    return request.session.get('carrito', {'establecimiento': None, 'items': {}})


def _carrito_items(request, establecimiento):
    carrito = _get_carrito(request)
    if not carrito.get('establecimiento') or int(carrito.get('establecimiento')) != establecimiento.id:
        return [], 0

    items_data = carrito.get('items', {})
    producto_ids = [int(pid) for pid, qty in items_data.items() if qty and int(qty) > 0]
    productos = Producto.objects.filter(id__in=producto_ids, establecimiento=establecimiento, disponible=True)

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


class ListaEstablecimientosView(ListView):
    model = Establecimiento
    template_name = 'establecimientos/lista_establecimientos.html'
    context_object_name = 'establecimientos'
    paginate_by = 12

    def get_queryset(self):
        return Establecimiento.objects.filter(activo=True)


class DetalleEstablecimientoView(DetailView):
    model = Establecimiento
    template_name = 'establecimientos/detalle_establecimiento.html'
    context_object_name = 'establecimiento'

    def get_queryset(self):
        return Establecimiento.objects.filter(activo=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = Producto.objects.filter(
            establecimiento=self.object,
            disponible=True
        )
        carrito_items, carrito_total = _carrito_items(self.request, self.object)
        context['carrito_items'] = carrito_items
        context['carrito_total'] = carrito_total
        return context