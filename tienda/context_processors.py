from .models import ItemCarrito

def carrito_context(request):
    """Context processor para mostrar el contador del carrito en todas las páginas"""
    if request.session.session_key:
        items_count = ItemCarrito.objects.filter(session_key=request.session.session_key).count()
    else:
        items_count = 0
    
    return {'carrito_items_count': items_count}