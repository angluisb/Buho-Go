from django.contrib import admin
from .models import Pedido, ItemPedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'establecimiento', 'estado', 'tipo_entrega', 'precio_total', 'creado_en']
    list_filter = ['estado', 'tipo_entrega', 'creado_en', 'establecimiento']
    search_fields = ['usuario__email', 'establecimiento__nombre']
    readonly_fields = ['creado_en', 'actualizado_en', 'precio_total']

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
    list_filter = ['pedido__estado', 'producto__establecimiento']
    search_fields = ['pedido__id', 'producto__nombre']
