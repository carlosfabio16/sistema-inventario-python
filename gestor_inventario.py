import sqlite3
from datetime import datetime # Necesario para guardar la fecha de venta

DB_NAME = "sistema_inventario.db"

def iniciar_db():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    
    # 1. Tabla de PRODUCTOS (Mejorada)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        codigo TEXT PRIMARY KEY,
        nombre TEXT NOT NULL,
        precio_venta INTEGER,
        precio_costo INTEGER,    -- Nuevo: Para calcular ganancias
        stock INTEGER,
        vencimiento TEXT         -- Nuevo: Fecha formato AAAA-MM-DD
    )
    """)
    
    # 2. Tabla de VENTAS (La Cabecera del ticket)
    # Guarda: Fecha, Total y Medio de Pago (Efectivo, Tarjeta, QR)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        total INTEGER,
        medio_pago TEXT
    )
    """)
    
    # 3. Tabla DETALLE_VENTA (El contenido del ticket)
    # Relaciona qué productos se fueron en qué venta
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detalle_ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_venta INTEGER,
        codigo_producto TEXT,
        cantidad INTEGER,
        subtotal INTEGER,
        ganancia INTEGER, -- Guardamos cuánto ganamos en este item específico
        FOREIGN KEY(id_venta) REFERENCES ventas(id)
    )
    """)
    
    conexion.commit()
    conexion.close()

def registrar_producto(codigo, nombre, precio_venta, precio_costo, stock, vencimiento):
    """
    Registra un producto con datos completos para gestión de inventario.
    """
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO productos VALUES (?, ?, ?, ?, ?, ?)", 
                       (codigo, nombre, precio_venta, precio_costo, stock, vencimiento))
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.IntegrityError:
        return False

def buscar_producto(codigo):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE codigo = ?", (codigo,))
    resultado = cursor.fetchone()
    conexion.close()
    
    if resultado:
        return {
            "codigo": resultado[0],
            "nombre": resultado[1],
            "precio_venta": resultado[2],
            "precio_costo": resultado[3], # Ahora devolvemos el costo también
            "stock": resultado[4],
            "vencimiento": resultado[5]
        }
    return None

def procesar_venta(carrito, medio_pago="EFECTIVO"):
    """
    Esta es la función CRÍTICA. 
    1. Resta Stock.
    2. Guarda el historial de venta para tus reportes futuros.
    """
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    
    try:
        # A. Calcular el total general
        total_venta = sum(item['subtotal'] for item in carrito)
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # B. Crear el registro en la tabla VENTAS (El Ticket)
        cursor.execute("INSERT INTO ventas (fecha, total, medio_pago) VALUES (?, ?, ?)",
                       (fecha_actual, total_venta, medio_pago))
        id_ticket = cursor.lastrowid # Obtenemos el ID del ticket recién creado (ej: Ticket #1)
        
        # C. Procesar cada producto
        for item in carrito:
            codigo = item['codigo']
            cantidad = item['cantidad']
            
            # 1. Obtener datos actuales del producto (necesitamos el costo y stock)
            cursor.execute("SELECT stock, precio_costo FROM productos WHERE codigo = ?", (codigo,))
            data_prod = cursor.fetchone()
            stock_actual = data_prod[0]
            costo_unitario = data_prod[1]
            
            # 2. Verificar Stock (Doble seguridad)
            if stock_actual < cantidad:
                raise Exception(f"Stock insuficiente para {item['nombre']}")
            
            # 3. Restar Stock
            nuevo_stock = stock_actual - cantidad
            cursor.execute("UPDATE productos SET stock = ? WHERE codigo = ?", (nuevo_stock, codigo))
            
            # 4. Guardar el DETALLE (para reportes de rotación y ganancia)
            ganancia_item = item['subtotal'] - (costo_unitario * cantidad)
            
            cursor.execute("""
                INSERT INTO detalle_ventas (id_venta, codigo_producto, cantidad, subtotal, ganancia)
                VALUES (?, ?, ?, ?, ?)
            """, (id_ticket, codigo, cantidad, item['subtotal'], ganancia_item))
            
        conexion.commit()
        conexion.close()
        return True, id_ticket # Devolvemos el número de ticket generado
        
    except Exception as e:
        print(f"ERROR CRÍTICO EN VENTA: {e}")
        conexion.rollback()
        conexion.close()
        return False, 0j
    

def obtener_reporte_dia():
    """Calcula ventas totales y ganancia bruta del día de hoy."""
    # Nota: Necesitas importar datetime arriba: from datetime import datetime
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    
    hoy = datetime.now().strftime("%Y-%m-%d") 
    
    # 1. Total Vendido
    cursor.execute("SELECT sum(total) FROM ventas WHERE fecha LIKE ?", (hoy + '%',))
    resultado_ventas = cursor.fetchone()[0]
    total_vendido = resultado_ventas if resultado_ventas else 0
    
    # 2. Total Ganancia
    cursor.execute("""
        SELECT sum(d.ganancia) 
        FROM detalle_ventas d
        JOIN ventas v ON d.id_venta = v.id
        WHERE v.fecha LIKE ?
    """, (hoy + '%',))
    resultado_ganancia = cursor.fetchone()[0]
    total_ganancia = resultado_ganancia if resultado_ganancia else 0
    
    conexion.close()
    return total_vendido, total_ganancia