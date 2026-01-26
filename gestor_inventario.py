# gestor_inventario.py

# 1. VARIABLE GLOBAL: Aquí vivirán los datos mientras el programa corre
inventario_global = {}

# 2. DEFINICIÓN DE FUNCIONES
def buscar_producto(codigo_barras):
    """
    Busca un código de barras en el inventario global.
    
    Args:
        codigo_barras (str): El código escaneado o escrito.
        
    Returns:
        dict: Los datos del producto si existe.
        None: Si el producto no existe (devuelve 'Nada').
    """
    # .get() es una forma segura de buscar en diccionarios.
    # Si existe devuelve el dato, si no, devuelve None.
    resultado = inventario_global.get(codigo_barras)
    return resultado

def registrar_producto(codigo, nombre, precio, cantidad_inicial):
    """
    Crea una nueva entrada en el inventario.
    
    Args:
        codigo (str): Identificador único.
        nombre (str): Descripción del producto.
        precio (int): Precio de venta.
        cantidad_inicial (int): Stock inicial.
        
    Returns:
        bool: True si se guardó con éxito, False si ya existía.
    """
    # 1. Validamos si ya existe este código
    if codigo in inventario_global:
        # Si existe, NO sobreescribimos. Devolvemos False como error.
        return False

    # 2. Creamos el diccionario interno
    datos_producto = {
        "nombre": nombre,
        "precio": precio,
        "stock": cantidad_inicial
    }
    
    # 3. Guardamos en el diccionario mayor
    inventario_global[codigo] = datos_producto
    return True # Devolvemos éxito

if __name__ == "__main__":
    print("--- INICIANDO TEST DE LÓGICA ---")
    
    # 1. Simulamos registrar un producto
    exito = registrar_producto("784001", "Galletita Tippy", 5000, 10)
    
    if exito:
        print("Prueba 1: Producto registrado correctamente.")
    else:
        print("Prueba 1: Falló el registro.")

    # 2. Probemos registrar EL MISMO producto (Debería fallar)
    exito_duplicado = registrar_producto("784001", "Galletita Tippy", 5000, 10)
    
    if not exito_duplicado:
        print("Prueba 2: El sistema evitó duplicados correctamente.")
    else:
        print("Prueba 2: Error, el sistema permitió duplicados.")
        
    # 3. Probemos buscar
    producto = buscar_producto("784001")
    if producto:
        print(f"Prueba 3: Datos recuperados -> {producto['nombre']} | Precio: {producto['precio']} | Stock: {producto['stock']}")