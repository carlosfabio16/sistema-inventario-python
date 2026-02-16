from django.db import models

class Producto(models.Model):
    # Definimos las columnas de la tabla (Django lo hará SQL automáticamente)
    codigo = models.CharField(max_length=20, unique=True, primary_key=True)
    nombre = models.CharField(max_length=100)
    precio_venta = models.IntegerField()
    precio_costo = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    # null=True significa que la base de datos acepta vacío
    # blank=True significa que el formulario web acepta dejarlo en blanco
    vencimiento = models.DateField(null=True, blank=True) 

    def __str__(self):
        # Esto define cómo se ve el producto en el menú (su nombre en vez de "Object 1")
        return f"{self.nombre} ({self.codigo})"