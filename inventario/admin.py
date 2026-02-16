from django.contrib import admin
from .models import Producto  # Importamos tu clase Producto

# Registramos la tabla para que el Admin la reconozca
admin.site.register(Producto)