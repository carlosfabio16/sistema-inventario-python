from django.http import HttpResponse

def saludo(request):
    return HttpResponse("<h1>¡Hola! Este es el inicio de mi Sistema de Inventario Web 📦</h1>")