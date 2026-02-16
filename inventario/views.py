from django.shortcuts import render
from .models import Producto # Importamos la tabla de productos

def escanear_producto(request):
    contexto = {} # Aquí guardaremos los datos para enviar al HTML

    if request.method == 'POST':
        # 1. Capturamos lo que envió el lector/teclado
        codigo_leido = request.POST.get('codigo_barras')
        
        # 2. Buscamos en la base de datos
        # filter().first() es una forma segura de buscar. Si no hay, devuelve None.
        producto = Producto.objects.filter(codigo=codigo_leido).first()

        if producto:
            # ¡Lo encontramos! Enviamos los datos al HTML
            contexto = {
                'mensaje': True,
                'encontrado': True,
                'nombre': producto.nombre,
                'precio': producto.precio_venta,
                'stock': producto.stock
            }
        else:
            # No existe. Enviamos aviso para crear.
            contexto = {
                'mensaje': True,
                'encontrado': False,
                'codigo': codigo_leido
            }

    return render(request, 'inventario/escanear.html', contexto)