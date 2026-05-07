from django.urls import path
from . import views

app_name = 'establecimientos'

urlpatterns = [
    path('', views.ListaEstablecimientosView.as_view(), name='lista_establecimientos'),
    path('mis-establecimientos/', views.MisEstablecimientosView.as_view(), name='mis_establecimientos'),
    path('crear/', views.CrearEstablecimientoView.as_view(), name='crear_establecimiento'),
    path('<int:establecimiento_id>/productos/crear/', views.CrearProductoView.as_view(), name='crear_producto'),
    path('<int:pk>/', views.DetalleEstablecimientoView.as_view(), name='detalle_establecimiento'),
]