from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from rest_framework import viewsets
from .models import Categoria, Producto, ItemCarrito
from .serializers import CategoriaSerializer, ProductoSerializer, ItemCarritoSerializer

# API ViewSets
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ItemCarritoViewSet(viewsets.ModelViewSet):
    queryset = ItemCarrito.objects.all()
    serializer_class = ItemCarritoSerializer

# Vistas HTML
def home(request):
    """Vista Home - Lista todos los productos"""
    productos = Producto.objects.filter(disponible=True)
    categorias = Categoria.objects.all()
    
    # Filtrar por categoría si se selecciona
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    context = {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_id
    }
    return render(request, 'tienda/home.html', context)

def detalle_producto(request, producto_id):
    """Vista DetalleProducto - Muestra información detallada del producto"""
    producto = get_object_or_404(Producto, id=producto_id)
    productos_relacionados = Producto.objects.filter(
        categoria=producto.categoria,
        disponible=True
    ).exclude(id=producto_id)[:4]
    
    context = {
        'producto': producto,
        'productos_relacionados': productos_relacionados
    }
    return render(request, 'tienda/detalle_producto.html', context)

def carrito(request):
    """Vista Carrito - Muestra los productos en el carrito"""
    if not request.session.session_key:
        request.session.create()
    
    session_key = request.session.session_key
    items = ItemCarrito.objects.filter(session_key=session_key)
    
    total = sum(item.get_subtotal() for item in items)
    
    context = {
        'items': items,
        'total': total
    }
    return render(request, 'tienda/carrito.html', context)

def agregar_al_carrito(request, producto_id):
    """Agregar producto al carrito"""
    if not request.session.session_key:
        request.session.create()
    
    producto = get_object_or_404(Producto, id=producto_id)
    session_key = request.session.session_key
    
    # Verificar si el producto ya está en el carrito
    item, created = ItemCarrito.objects.get_or_create(
        session_key=session_key,
        producto=producto,
        defaults={'cantidad': 1}
    )
    
    if not created:
        item.cantidad += 1
        item.save()
    
    messages.success(request, f'{producto.nombre} agregado al carrito')
    return redirect('carrito')

def actualizar_carrito(request, item_id):
    """Actualizar cantidad de un item en el carrito"""
    item = get_object_or_404(ItemCarrito, id=item_id)
    cantidad = int(request.POST.get('cantidad', 1))
    
    if cantidad > 0:
        item.cantidad = cantidad
        item.save()
        messages.success(request, 'Carrito actualizado')
    else:
        item.delete()
        messages.success(request, 'Producto eliminado del carrito')
    
    return redirect('carrito')

def eliminar_del_carrito(request, item_id):
    """Eliminar un item del carrito"""
    item = get_object_or_404(ItemCarrito, id=item_id)
    item.delete()
    messages.success(request, 'Producto eliminado del carrito')
    return redirect('carrito')