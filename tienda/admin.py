from django.contrib import admin
from .models import Categoria, Producto, ItemCarrito

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'creado']
    search_fields = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'autor', 'precio', 'stock', 'disponible', 'creado']
    list_filter = ['categoria', 'disponible', 'creado']
    search_fields = ['nombre', 'autor', 'isbn']
    list_editable = ['precio', 'stock', 'disponible']

@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ['producto', 'cantidad', 'session_key', 'fecha_agregado']
    list_filter = ['fecha_agregado']