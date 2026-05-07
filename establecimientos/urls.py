from django.urls import path
from . import views

app_name = 'establecimientos'

urlpatterns = [

    path(
        '',
        views.ListaEstablecimientosView.as_view(),
        name='lista_establecimientos'
    ),

    path(
        '<int:pk>/',
        views.DetalleEstablecimientoView.as_view(),
        name='detalle_establecimiento'
    ),

]