from rest_framework import serializers
from .models import Categoria, Producto, ItemCarrito

class CategoriaSerializer(serializers.ModelSerializer):
    total_productos = serializers.SerializerMethodField()
    imagen = serializers.SerializerMethodField()
    
    class Meta:
        model = Categoria
        fields = '__all__'
    
    def get_total_productos(self, obj):
        return obj.productos.filter(disponible=True).count()
    
    def get_imagen(self, obj):
        if obj.imagen:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.imagen.url)
            return f"http://localhost:8000{obj.imagen.url}"
        return None

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    precio_final = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    tiene_descuento = serializers.BooleanField(read_only=True)
    porcentaje_descuento = serializers.IntegerField(read_only=True)
    imagen = serializers.SerializerMethodField()
    
    class Meta:
        model = Producto
        fields = '__all__'
    
    def get_imagen(self, obj):
        if obj.imagen:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.imagen.url)
            return f"http://localhost:8000{obj.imagen.url}"
        return None

class ProductoListSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    precio_final = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    tiene_descuento = serializers.BooleanField(read_only=True)
    porcentaje_descuento = serializers.IntegerField(read_only=True)
    imagen = serializers.SerializerMethodField()
    
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'autor', 'categoria', 'categoria_nombre', 'precio', 
                  'precio_descuento', 'precio_final', 'tiene_descuento', 'porcentaje_descuento',
                  'stock', 'imagen', 'disponible', 'destacado', 'nuevo']
    
    def get_imagen(self, obj):
        if obj.imagen:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.imagen.url)
            return f"http://localhost:8000{obj.imagen.url}"
        return None

class ItemCarritoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    producto_precio = serializers.DecimalField(source='producto.precio_final', max_digits=10, decimal_places=2, read_only=True)
    producto_imagen = serializers.SerializerMethodField()
    producto_stock = serializers.IntegerField(source='producto.stock', read_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = ItemCarrito
        fields = ['id', 'producto', 'producto_nombre', 'producto_precio', 'producto_imagen', 
                  'producto_stock', 'cantidad', 'subtotal', 'fecha_agregado']
        read_only_fields = ['fecha_agregado']
    
    def get_producto_imagen(self, obj):
        if obj.producto.imagen:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.producto.imagen.url)
            return f"http://localhost:8000{obj.producto.imagen.url}"
        return None
    
    def get_subtotal(self, obj):
        return obj.get_subtotal()

class AgregarCarritoSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField()
    cantidad = serializers.IntegerField(default=1, min_value=1)
    
    def validate_producto_id(self, value):
        try:
            producto = Producto.objects.get(id=value)
            if not producto.disponible:
                raise serializers.ValidationError('Producto no disponible')
            return value
        except Producto.DoesNotExist:
            raise serializers.ValidationError('Producto no encontrado')
    
    def validate(self, data):
        producto = Producto.objects.get(id=data['producto_id'])
        if data['cantidad'] > producto.stock:
            raise serializers.ValidationError(
                f'Stock insuficiente. Disponible: {producto.stock}'
            )
        return data

class ActualizarCantidadSerializer(serializers.Serializer):
    cantidad = serializers.IntegerField(min_value=1)
    
    def validate_cantidad(self, value):
        item = self.context.get('item')
        if item and value > item.producto.stock:
            raise serializers.ValidationError(
                f'Stock insuficiente. Disponible: {item.producto.stock}'
            )
        return value