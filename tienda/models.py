from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=200)
    autor = models.CharField(max_length=200, blank=True)
    editorial = models.CharField(max_length=100, blank=True)
    isbn = models.CharField(max_length=13, blank=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_descuento = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    disponible = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    nuevo = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-creado']
    
    def __str__(self):
        return self.nombre
    
    def tiene_descuento(self):
        return self.precio_descuento is not None and self.precio_descuento < self.precio
    
    def precio_final(self):
        if self.tiene_descuento():
            return self.precio_descuento
        return self.precio
    
    def porcentaje_descuento(self):
        if self.tiene_descuento():
            descuento = ((self.precio - self.precio_descuento) / self.precio) * 100
            return round(descuento)
        return 0

class ItemCarrito(models.Model):
    session_key = models.CharField(max_length=40)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Item del Carrito'
        verbose_name_plural = 'Items del Carrito'
        unique_together = ('session_key', 'producto')
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    
    def get_subtotal(self):
        return self.producto.precio_final() * self.cantidad
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.cantidad > self.producto.stock:
            raise ValidationError(f'Stock insuficiente. Disponible: {self.producto.stock}')