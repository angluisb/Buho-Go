from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Establecimiento, Producto

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
        return context
