import os
import gestor_inventario as cerebro

def limpiar_pantalla():
    """Limpia la consola para que se vea ordenado."""
    os.system('cls' if os.name == 'nt' else 'clear')

def modo_caja():
    """
    Módulo de Punto de Venta (POS).
    Permite escanear múltiples productos y generar un ticket de venta.
    """
    print("\n🛒 --- MODO CAJA (PUNTO DE VENTA) ---")
    print("Escanea productos. Escribe 'FIN' para cobrar.")
    
    carrito = [] 
    total_a_pagar = 0
    
    while True:
        codigo = input("\nEscanee producto: ").strip()
        
        # Si el cajero escribe FIN, terminamos de escanear
        if codigo.upper() == 'FIN':
            break 
            
        producto = cerebro.buscar_producto(codigo)
        
        if producto:
            print(f"   -> {producto['nombre']} | Gs. {producto['precio_venta']}")
            
            # Por ahora cantidad es 1, más adelante podemos preguntar "¿Cuántos?"
            cantidad = 1 
            subtotal = producto['precio_venta'] * cantidad
            
            # Agregamos al carrito temporal
            item = {
                "codigo": codigo,
                "nombre": producto['nombre'],
                "precio": producto['precio_venta'],
                "cantidad": cantidad,
                "subtotal": subtotal
            }
            carrito.append(item)
            total_a_pagar += subtotal
            
            print(f"   ✅ Agregado. Subtotal acumulado: Gs. {total_a_pagar}")
        else:
            print("   ❌ Producto no encontrado o sin stock.")

    # --- MOMENTO DEL COBRO ---
    if len(carrito) > 0:
        print("\n=================================")
        print(f"💰 TOTAL A PAGAR: Gs. {total_a_pagar}")
        print("=================================")
        confirmacion = input("¿Confirmar venta y descontar stock? (S/N): ")
        
        if confirmacion.upper() == 'S':
            # Llamamos al cerebro para que guarde la venta y reste stock
            exito, id_ticket = cerebro.procesar_venta(carrito)
            
            if exito:
                print(f"\n✅ ¡VENTA REALIZADA! Ticket #{id_ticket} generado.")
            else:
                print("\n❌ Error al guardar la venta en base de datos.")
        else:
            print("\n🚫 Venta cancelada.")
    else:
        print("\n🚫 Carrito vacío.")

def iniciar_sistema():
    # Aseguramos que la base de datos exista al arrancar
    cerebro.iniciar_db()
    
    while True:
        limpiar_pantalla()
        print("=== SISTEMA DE GESTIÓN COMERCIAL ===")
        print("1. 📦 Modo Inventario (Cargar Productos)")
        print("2. 🛒 Modo Caja (Vender)")
        print("3. 📊 Reporte Financiero del Día")
        print("4. Salir")
        
        opcion = input("\nElige una opción: ")
        
        if opcion == "1":
            print("\n--- ALTA DE PRODUCTOS ---")
            codigo = input("Código de Barras: ").strip()
            
            # Buscamos si ya existe para no duplicar
            producto_existente = cerebro.buscar_producto(codigo)
            
            if producto_existente:
                print(f"⚠️ El producto '{producto_existente['nombre']}' ya existe.")
                print(f"Stock actual: {producto_existente['stock']}")
                # Aquí podrías agregar lógica para sumar stock si quisieras
            else:
                nombre = input("Nombre del Producto: ")
                try:
                    # AQUÍ ESTÁN LOS CAMPOS NUEVOS (Costo y Vencimiento)
                    precio = int(input("Precio de VENTA: "))
                    costo = int(input("Precio de COSTO (Compra): ")) 
                    stock_inicial = int(input("Stock Inicial: "))
                    vencimiento = input("Fecha de Vencimiento (YYYY-MM-DD): ")
                    
                    # Enviamos todo al cerebro
                    cerebro.registrar_producto(codigo, nombre, precio, costo, stock_inicial, vencimiento)
                    print("\n💾 Producto guardado exitosamente.")
                    
                except ValueError:
                    print("\n❌ Error: Los precios y stock deben ser números enteros.")
            
            input("\nEnter para volver...")
            
        elif opcion == "2":
            modo_caja()
            input("\nEnter para volver al menú...")

        elif opcion == "3":
            # Llamamos a la función de reporte que creamos
            vendido, ganado = cerebro.obtener_reporte_dia()
            
            print("\n📊 --- REPORTE DE HOY ---")
            print(f"💰 Ventas Totales:   Gs. {vendido}")
            print(f"📈 Ganancia Bruta:   Gs. {ganado}")
            
            if vendido > 0:
                margen = (ganado / vendido) * 100
                print(f"✨ Margen de Rentabilidad: {margen:.1f}%")
            else:
                print("No hubo ventas hoy.")
                
            input("\nEnter para volver...")
            
        elif opcion == "4":
            print("Cerrando sistema... ¡Buenas ventas!")
            break

if __name__ == "__main__":
    iniciar_sistema()