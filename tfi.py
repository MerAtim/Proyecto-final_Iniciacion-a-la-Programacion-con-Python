# Trabajo Final Integrador - Sistema de gestión de inventario
# Este programa permite, mediante un menú en la terminal:
# 1. Registrar nuevos productos
# 2. Visualizar los productos registrados
# 3. Actualizar un producto mediante su ID
# 4. Eliminar un producto mediante su ID
# 5. Buscar productos por ID, nombre o categoría
# 6. Generar un reporte de productos con stock bajo
# 7. Salir
#
# Los datos se guardan en una base de datos SQLite llamada 'inventario.db'.

import os
import sqlite3

# Colorama es opcional: si no está instalado, el programa funciona igual pero sin colores.
try:
    from colorama import Fore, Style, init  #type: ignore

    init(autoreset=True)
except ImportError:
    class _SinColor:
        # Devuelve un texto vacío para cualquier color pedido (Fore.RED, Style.BRIGHT, etc.)
        def __getattr__(self, nombre):
            return ""

    Fore = Style = _SinColor()

# La base de datos se crea en la misma carpeta que este archivo
RUTA_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventario.db")

#                       MENSAJES CON COLOR

def mensaje_exito(texto):
    print(Fore.GREEN + texto)


def mensaje_error(texto):
    print(Fore.RED + texto)


def mensaje_aviso(texto):
    print(Fore.YELLOW + texto)


def titulo(texto):
    print("\n" + Fore.CYAN + Style.BRIGHT + f"--- {texto} ---")


#                         BASE DE DATOS

def conectar():
    """Abre y devuelve una conexión a la base de datos."""
    return sqlite3.connect(RUTA_DB)


def crear_tabla():
    """Crea la tabla 'productos' si todavía no existe."""
    conexion = conectar()
    try:
        cursor = conexion.cursor()
        # CHECK evita cantidades o precios negativos directamente desde la base de datos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre      TEXT    NOT NULL,
                descripcion TEXT,
                cantidad    INTEGER NOT NULL CHECK (cantidad >= 0),
                precio      REAL    NOT NULL CHECK (precio >= 0),
                categoria   TEXT
            )
        """)
        conexion.commit()
    finally:
        conexion.close()


def obtener_producto_por_id(id_producto):
    """Devuelve la fila del producto con ese ID, o None si no existe."""
    conexion = conectar()
    try:
        cursor = conexion.cursor()
        # Consulta parametrizada (?) para prevenir inyecciones SQL
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        return cursor.fetchone()
    finally:
        conexion.close()


def existe_nombre(nombre, id_excluido=None):
    """
    Indica si ya hay un producto con ese nombre (sin distinguir mayúsculas).
    id_excluido permite ignorar al propio producto cuando se está actualizando.
    """
    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id FROM productos WHERE LOWER(nombre) = LOWER(?) AND id != ?",
            (nombre, id_excluido if id_excluido is not None else -1),
        )
        return cursor.fetchone() is not None
    finally:
        conexion.close()


#                     VALIDACIÓN DE ENTRADAS

def pedir_texto(mensaje, obligatorio=True, valor_actual=None, requiere_letras=False):
    """
    Pide un texto al usuario.
    - Si es obligatorio, no acepta un texto vacío.
    - Si se pasa valor_actual (modo actualización), Enter conserva ese valor.
    - Si requiere_letras es True, el texto debe contener al menos una letra
      (evita nombres como "1" o "123", pero acepta "Lámpara 10W").
    """
    while True:
        texto = input(mensaje).strip()
        if texto == "" and valor_actual is not None:
            return valor_actual
        if texto == "" and obligatorio:
            mensaje_error("Este campo no puede estar vacío. Intente de nuevo.")
            continue
        if texto != "" and requiere_letras and not any(caracter.isalpha() for caracter in texto):
            mensaje_error("Este campo debe contener al menos una letra. Intente de nuevo.")
            continue
        return texto


def pedir_nombre(mensaje, valor_actual=None, id_producto=None):
    """Pide el nombre de un producto y verifica que no esté repetido."""
    while True:
        nombre = pedir_texto(mensaje, valor_actual=valor_actual, requiere_letras=True).title()
        if existe_nombre(nombre, id_excluido=id_producto):
            mensaje_error(f"Ya existe un producto llamado '{nombre}'. Ingrese otro nombre "
                          "(o use 'Actualizar producto' para modificar el existente).")
            continue
        return nombre


def pedir_entero(mensaje, minimo=0, valor_actual=None):
    """Pide un número entero mayor o igual a 'minimo'."""
    while True:
        texto = input(mensaje).strip()
        if texto == "" and valor_actual is not None:
            return valor_actual
        try:
            numero = int(texto)
        except ValueError:
            mensaje_error("Ingrese un número entero válido.")
            continue
        if numero < minimo:
            mensaje_error(f"El número debe ser mayor o igual a {minimo}.")
            continue
        return numero


def pedir_real(mensaje, minimo=0, valor_actual=None):
    """Pide un número real (acepta coma o punto decimal) mayor o igual a 'minimo'."""
    while True:
        texto = input(mensaje).strip().replace(",", ".")
        if texto == "" and valor_actual is not None:
            return valor_actual
        try:
            numero = float(texto)
        except ValueError:
            mensaje_error("Ingrese un número válido (ej: 1500 o 1500.50).")
            continue
        if numero < minimo:
            mensaje_error(f"El número debe ser mayor o igual a {minimo}.")
            continue
        return numero


def pedir_confirmacion(mensaje):
    """Devuelve True si el usuario responde 's' y False si responde 'n'."""
    while True:
        respuesta = input(mensaje + " (s/n): ").strip().lower()
        if respuesta in ("s", "n"):
            return respuesta == "s"
        mensaje_error("Responda 's' para sí o 'n' para no.")


#                     PRESENTACIÓN DE DATOS


def mostrar_tabla(productos):
    """Imprime una lista de productos en formato de tabla."""
    encabezado = f"{'ID':<5}{'Nombre':<20}{'Descripción':<28}{'Cant.':>7}{'Precio':>13}  {'Categoría':<15}"
    print(Style.BRIGHT + encabezado)
    print("-" * len(encabezado))
    for id_producto, nombre, descripcion, cantidad, precio, categoria in productos:
        # Recortamos textos largos para que no rompan la tabla
        print(f"{id_producto:<5}{nombre[:19]:<20}{(descripcion or '-')[:27]:<28}"
              f"{cantidad:>7}{'$' + format(precio, ',.2f'):>13}  {(categoria or '-')[:15]:<15}")
    print("-" * len(encabezado))
    print(f"Total: {len(productos)} producto(s)")


def mostrar_producto(producto):
    """Muestra el detalle de un único producto."""
    id_producto, nombre, descripcion, cantidad, precio, categoria = producto
    print(f"ID:          {id_producto}")
    print(f"Nombre:      {nombre}")
    print(f"Descripción: {descripcion or '-'}")
    print(f"Cantidad:    {cantidad}")
    print(f"Precio:      ${precio:,.2f}")
    print(f"Categoría:   {categoria or '-'}")


#                       FUNCIONALIDADES (ABM)

def registrar_producto():
    """Solicita los datos de un producto nuevo y lo guarda en la base de datos."""
    titulo("Registrar producto")

    nombre = pedir_nombre("Nombre: ")
    descripcion = pedir_texto("Descripción (opcional): ", obligatorio=False)
    cantidad = pedir_entero("Cantidad: ", minimo=0)
    precio = pedir_real("Precio: $", minimo=0)
    categoria = pedir_texto("Categoría (opcional): ", obligatorio=False, requiere_letras=True).title()

    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) "
            "VALUES (?, ?, ?, ?, ?)",
            (nombre, descripcion, cantidad, precio, categoria),
        )
        conexion.commit()
        mensaje_exito(f"Producto '{nombre}' registrado con ID {cursor.lastrowid}.")
    except sqlite3.Error as error:
        mensaje_error(f"No se pudo registrar el producto: {error}")
    finally:
        conexion.close()


def visualizar_productos():
    """Muestra todos los productos registrados."""
    titulo("Productos registrados")

    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos ORDER BY id")
        productos = cursor.fetchall()
    except sqlite3.Error as error:
        mensaje_error(f"No se pudieron consultar los productos: {error}")
        return
    finally:
        conexion.close()

    if not productos:
        mensaje_aviso("No hay productos registrados.")
    else:
        mostrar_tabla(productos)


def actualizar_producto():
    """Modifica los datos de un producto existente, buscándolo por su ID."""
    titulo("Actualizar producto")

    id_producto = pedir_entero("ID del producto a actualizar: ", minimo=1)
    producto = obtener_producto_por_id(id_producto)
    if producto is None:
        mensaje_aviso(f"No existe un producto con ID {id_producto}.")
        return

    mostrar_producto(producto)
    print(Fore.CYAN + "\nIngrese los nuevos datos (presione Enter para conservar el valor actual):")

    _, nombre, descripcion, cantidad, precio, categoria = producto
    nombre = pedir_nombre(f"Nombre [{nombre}]: ", valor_actual=nombre, id_producto=id_producto)
    descripcion = pedir_texto(f"Descripción [{descripcion or '-'}]: ", valor_actual=descripcion)
    cantidad = pedir_entero(f"Cantidad [{cantidad}]: ", minimo=0, valor_actual=cantidad)
    precio = pedir_real(f"Precio [${precio:,.2f}]: $", minimo=0, valor_actual=precio)
    categoria = pedir_texto(f"Categoría [{categoria or '-'}]: ", valor_actual=categoria,
                            requiere_letras=True).title()

    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE productos SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ? "
            "WHERE id = ?",
            (nombre, descripcion, cantidad, precio, categoria, id_producto),
        )
        conexion.commit()
        mensaje_exito(f"Producto con ID {id_producto} actualizado correctamente.")
    except sqlite3.Error as error:
        mensaje_error(f"No se pudo actualizar el producto: {error}")
    finally:
        conexion.close()


def eliminar_producto():
    """Elimina un producto por su ID, previa confirmación."""
    titulo("Eliminar producto")

    id_producto = pedir_entero("ID del producto a eliminar: ", minimo=1)
    producto = obtener_producto_por_id(id_producto)
    if producto is None:
        mensaje_aviso(f"No existe un producto con ID {id_producto}.")
        return

    mostrar_producto(producto)
    if not pedir_confirmacion(Fore.YELLOW + "\n¿Seguro que desea eliminar este producto?"):
        mensaje_aviso("Eliminación cancelada.")
        return

    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        conexion.commit()
        mensaje_exito(f"Producto '{producto[1]}' eliminado correctamente.")
    except sqlite3.Error as error:
        mensaje_error(f"No se pudo eliminar el producto: {error}")
    finally:
        conexion.close()


def buscar_producto():
    """Busca productos por ID (exacto), por nombre o por categoría (coincidencia parcial)."""
    titulo("Buscar producto")
    print("1. Buscar por ID")
    print("2. Buscar por nombre")
    print("3. Buscar por categoría")
    opcion = input("Elija una opción (1-3): ").strip()

    if opcion == "1":
        id_producto = pedir_entero("ID del producto: ", minimo=1)
        producto = obtener_producto_por_id(id_producto)
        if producto is None:
            mensaje_aviso(f"No existe un producto con ID {id_producto}.")
        else:
            print()
            mostrar_producto(producto)
        return

    if opcion == "2":
        campo = "nombre"
    elif opcion == "3":
        campo = "categoria"
    else:
        mensaje_error("Opción inválida.")
        return

    texto = pedir_texto(f"Texto a buscar en {campo}: ")

    conexion = conectar()
    try:
        cursor = conexion.cursor()
        # 'campo' sólo puede valer "nombre" o "categoria" (lo elegimos nosotros arriba),
        # y el texto del usuario va siempre como parámetro (?), nunca dentro del SQL.
        # LIKE con % permite coincidencias parciales y no distingue mayúsculas.
        cursor.execute(
            f"SELECT * FROM productos WHERE {campo} LIKE ? ORDER BY id",
            (f"%{texto}%",),
        )
        productos = cursor.fetchall()
    except sqlite3.Error as error:
        mensaje_error(f"No se pudo realizar la búsqueda: {error}")
        return
    finally:
        conexion.close()

    if not productos:
        mensaje_aviso(f"No se encontraron productos para '{texto}'.")
    else:
        mostrar_tabla(productos)


def reporte_bajo_stock():
    """Muestra los productos con cantidad igual o inferior a un límite indicado por el usuario."""
    titulo("Reporte de bajo stock")

    limite = pedir_entero("Mostrar productos con cantidad menor o igual a: ", minimo=0)

    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT * FROM productos WHERE cantidad <= ? ORDER BY cantidad, id",
            (limite,),
        )
        productos = cursor.fetchall()
    except sqlite3.Error as error:
        mensaje_error(f"No se pudo generar el reporte: {error}")
        return
    finally:
        conexion.close()

    if not productos:
        mensaje_exito(f"No hay productos con cantidad menor o igual a {limite}.")
    else:
        mostrar_tabla(productos)


#                          MENÚ PRINCIPAL

def mostrar_menu():
    print("\n" + Fore.CYAN + Style.BRIGHT + "--------------------------------")
    print(Fore.CYAN + Style.BRIGHT + "   Sistema de gestión de inventario")
    print(Fore.CYAN + Style.BRIGHT + "--------------------------------")
    print("1. Registrar producto")
    print("2. Visualizar productos")
    print("3. Actualizar producto")
    print("4. Eliminar producto")
    print("5. Buscar producto")
    print("6. Reporte de bajo stock")
    print("7. Salir")


def main():
    # Nos aseguramos de que la base de datos y la tabla existan antes de empezar
    try:
        crear_tabla()
    except sqlite3.Error as error:
        mensaje_error(f"No se pudo inicializar la base de datos: {error}")
        return

    # Cada opción del menú se asocia con la función que la resuelve
    opciones = {
        "1": registrar_producto,
        "2": visualizar_productos,
        "3": actualizar_producto,
        "4": eliminar_producto,
        "5": buscar_producto,
        "6": reporte_bajo_stock,
    }

    while True:
        mostrar_menu()
        opcion = input("Elija una opción (1-7): ").strip()

        if opcion == "7":
            mensaje_exito("\nGracias por usar el sistema. ¡Hasta luego!")
            break
        elif opcion in opciones:
            opciones[opcion]()
        else:
            mensaje_error("Opción inválida. Elija un número del 1 al 7.")


# Sólo se ejecuta el menú si el archivo se corre directamente
if __name__ == "__main__":
    main()
