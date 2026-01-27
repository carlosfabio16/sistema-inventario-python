# main.py
import os
import gestor_inventario as cerebro # Importamos nuestro otro archivo y le ponemos de nombre 'cerebro'

def limpiar_pantalla():
    # Para borrar la consola y que se vea ordenado
    os.system('cls' if os.name == 'nt' else 'clear')

def iniciar_sistema():
    print("=========================================")
    print("   SISTEMA DE CONTROL DE STOCK (V 0.1)   ")
    print("=========================================")
    print("Usa el Lector de Barras o escribe manual.")
    print("Escribe 'SALIR' para cerrar.")

    while True:
        print("\n--- ESPERANDO LECTURA ---")
        # 1. Aquí es donde el Lector de Barras "dispara" el texto + Enter
        codigo = input("Escanee código: ").strip() # .strip() quita espacios vacíos accidentales
        
        if codigo.upper() == 'SALIR':
            print("Cerrando sistema...")
            break
        
        if not codigo:
            continue # Si presionaron Enter sin escribir nada, ignora.

        # 2. Preguntamos al cerebro si el producto existe
        producto = cerebro.buscar_producto(codigo)

        if producto:
            # --- ESCENARIO A: PRODUCTO CONOCIDO (ACTUALIZAR) ---
            print(f"PRODUCTO: {producto['nombre']}")
            print(f"Stock Actual: {producto['stock']} | Precio: {producto['precio']}")
            
            try:
                entrada = input("¿Cantidad a ingresar? (Dejar vacío para cancelar): ")
                if entrada:
                    cantidad = int(entrada)
                    nuevo_total = cerebro.actualizar_stock(codigo, cantidad)
                    print(f"LISTO. Nuevo Stock: {nuevo_total}")
                else:
                    print("Operación cancelada.")
            except ValueError:
                print("ERROR: Debes ingresar un número entero.")

        else:
            # --- ESCENARIO B: PRODUCTO NUEVO (REGISTRAR) ---
            print("CÓDIGO NUEVO DETECTADO")
            print("Ingrese los datos para dar de alta:")
            
            nombre = input("Nombre/Descripción: ")
            
            # Validación simple de precio
            try:
                precio = int(input("Precio de Venta: "))
                stock_inicial = int(input("Stock Inicial: "))
                
                # Llamamos a la función de registro del cerebro
                cerebro.registrar_producto(codigo, nombre, precio, stock_inicial)
                print("Producto guardado exitosamente.")
                
            except ValueError:
                print("ERROR: Precio y Stock deben ser números.")

if __name__ == "__main__":
    iniciar_sistema()