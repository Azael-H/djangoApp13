from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Categoria, Producto, ItemCarrito
from .serializers import (
    CategoriaSerializer, ProductoSerializer, ProductoListSerializer,
    ItemCarritoSerializer, AgregarCarritoSerializer, ActualizarCantidadSerializer
)

class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.filter(activo=True)
    serializer_class = CategoriaSerializer
    
    @action(detail=True, methods=['get'])
    def productos(self, request, pk=None):
        categoria = self.get_object()
        productos = Producto.objects.filter(categoria=categoria, disponible=True)
        serializer = ProductoListSerializer(productos, many=True)
        return Response(serializer.data)

class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Producto.objects.filter(disponible=True)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductoListSerializer
        return ProductoSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        categoria = self.request.query_params.get('categoria', None)
        busqueda = self.request.query_params.get('busqueda', None)
        destacados = self.request.query_params.get('destacados', None)
        nuevos = self.request.query_params.get('nuevos', None)
        
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)
        
        if busqueda:
            queryset = queryset.filter(
                Q(nombre__icontains=busqueda) |
                Q(autor__icontains=busqueda) |
                Q(descripcion__icontains=busqueda)
            )
        
        if destacados == 'true':
            queryset = queryset.filter(destacado=True)
        
        if nuevos == 'true':
            queryset = queryset.filter(nuevo=True)
        
        return queryset

class CarritoViewSet(viewsets.ViewSet):
    
    def _get_session_key(self, request):
        if not request.session.session_key:
            request.session.create()
        return request.session.session_key
    
    def list(self, request):
        session_key = self._get_session_key(request)
        items = ItemCarrito.objects.filter(session_key=session_key)
        serializer = ItemCarritoSerializer(items, many=True)
        
        total = sum(item.get_subtotal() for item in items)
        
        return Response({
            'items': serializer.data,
            'total': total,
            'cantidad_items': items.count()
        })
    
    def create(self, request):
        serializer = AgregarCarritoSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        session_key = self._get_session_key(request)
        producto_id = serializer.validated_data['producto_id']
        cantidad = serializer.validated_data['cantidad']
        
        producto = Producto.objects.get(id=producto_id)
        
        item, created = ItemCarrito.objects.get_or_create(
            session_key=session_key,
            producto=producto,
            defaults={'cantidad': cantidad}
        )
        
        if not created:
            nueva_cantidad = item.cantidad + cantidad
            if nueva_cantidad > producto.stock:
                return Response(
                    {'error': f'Stock insuficiente. Disponible: {producto.stock}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            item.cantidad = nueva_cantidad
            item.save()
        
        item_serializer = ItemCarritoSerializer(item)
        return Response(item_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['put'])
    def actualizar_cantidad(self, request, pk=None):
        session_key = self._get_session_key(request)
        item = get_object_or_404(ItemCarrito, pk=pk, session_key=session_key)
        
        serializer = ActualizarCantidadSerializer(
            data=request.data,
            context={'item': item}
        )
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        item.cantidad = serializer.validated_data['cantidad']
        item.save()
        
        item_serializer = ItemCarritoSerializer(item)
        return Response(item_serializer.data)
    
    def destroy(self, request, pk=None):
        session_key = self._get_session_key(request)
        item = get_object_or_404(ItemCarrito, pk=pk, session_key=session_key)
        item.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['delete'])
    def limpiar(self, request):
        session_key = self._get_session_key(request)
        ItemCarrito.objects.filter(session_key=session_key).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def home(request):
    productos = Producto.objects.filter(disponible=True)
    categorias = Categoria.objects.filter(activo=True)
    
    categoria_id = request.GET.get('categoria')
    busqueda = request.GET.get('busqueda')
    
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) |
            Q(autor__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )
    
    context = {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_id,
        'busqueda': busqueda
    }
    return render(request, 'tienda/home.html', context)

def detalle_producto(request, producto_id):
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
    if not request.session.session_key:
        request.session.create()
    
    producto = get_object_or_404(Producto, id=producto_id)
    session_key = request.session.session_key
    
    item, created = ItemCarrito.objects.get_or_create(
        session_key=session_key,
        producto=producto,
        defaults={'cantidad': 1}
    )
    
    if not created:
        if item.cantidad + 1 > producto.stock:
            messages.error(request, f'Stock insuficiente. Disponible: {producto.stock}')
        else:
            item.cantidad += 1
            item.save()
            messages.success(request, f'{producto.nombre} agregado al carrito')
    else:
        messages.success(request, f'{producto.nombre} agregado al carrito')
    
    return redirect('carrito')

def actualizar_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    cantidad = int(request.POST.get('cantidad', 1))
    
    if cantidad > 0:
        if cantidad > item.producto.stock:
            messages.error(request, f'Stock insuficiente. Disponible: {item.producto.stock}')
        else:
            item.cantidad = cantidad
            item.save()
            messages.success(request, 'Carrito actualizado')
    else:
        item.delete()
        messages.success(request, 'Producto eliminado del carrito')
    
    return redirect('carrito')

def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    item.delete()
    messages.success(request, 'Producto eliminado del carrito')
    return redirect('carrito')

def categorias(request):
    categorias = Categoria.objects.filter(activo=True)
    context = {
        'categorias': categorias
    }
    return render(request, 'tienda/categorias.html', context)

def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id, activo=True)
    productos = Producto.objects.filter(categoria=categoria, disponible=True)
    
    context = {
        'categoria': categoria,
        'productos': productos
    }
    return render(request, 'tienda/productos_categoria.html', context)