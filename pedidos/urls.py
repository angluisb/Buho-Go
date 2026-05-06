from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    # URLs para estudiantes
    path('mis-pedidos/', views.MisPedidosView.as_view(), name='mis_pedidos'),
    path('<int:pk>/', views.DetallePedidoView.as_view(), name='detalle_pedido'),
    path('crear/<int:establecimiento_id>/', views.crear_pedido, name='crear_pedido'),

    # URLs para personal del establecimiento
    path('gestionar/', views.GestionarPedidosView.as_view(), name='gestionar_pedidos'),
    path('<int:pk>/actualizar-estado/', views.ActualizarEstadoPedidoView.as_view(), name='actualizar_estado'),
]