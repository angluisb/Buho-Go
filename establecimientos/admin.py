from django.contrib import admin
from .models import Establecimiento, Producto

@admin.register(Establecimiento)
class EstablecimientoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'direccion', 'telefono', 'activo', 'creado_en']
    list_filter = ['activo', 'creado_en']
    search_fields = ['nombre', 'direccion', 'telefono']
    readonly_fields = ['creado_en', 'actualizado_en']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'establecimiento', 'precio', 'disponible', 'creado_en']
    list_filter = ['disponible', 'establecimiento', 'creado_en']
    search_fields = ['nombre', 'establecimiento__nombre']
    readonly_fields = ['creado_en', 'actualizado_en']
    list_editable = ['precio', 'disponible']
