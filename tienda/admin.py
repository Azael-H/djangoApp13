from django.contrib import admin
from .models import Categoria, Producto, ItemCarrito

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'creado']
    search_fields = ['nombre']
    list_filter = ['activo', 'creado']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'autor', 'precio', 'precio_descuento', 'stock', 'disponible', 'destacado', 'nuevo', 'creado']
    list_filter = ['categoria', 'disponible', 'destacado', 'nuevo', 'creado']
    search_fields = ['nombre', 'autor', 'isbn']
    list_editable = ['precio', 'precio_descuento', 'stock', 'disponible', 'destacado', 'nuevo']

@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ['producto', 'cantidad', 'session_key', 'fecha_agregado', 'get_subtotal']
    list_filter = ['fecha_agregado']
    
    def get_subtotal(self, obj):
        return f'S/. {obj.get_subtotal()}'
    get_subtotal.short_description = 'Subtotal'