# Módulo con las consultas a la base de datos.
# Estas funciones no piden ni muestran nada por pantalla: solo leen o escriben en la tabla 'productos'.
# Todas usan consultas parametrizadas (?) para prevenir inyecciones SQL.

from conexion import conectar


def registrar_producto(nombre, descripcion, cantidad, precio, categoria):
    """Inserta un producto nuevo y devuelve el ID que se le asignó."""
    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) "
            "VALUES (?, ?, ?, ?, ?)",
            (nombre, descripcion, cantidad, precio, categoria),
        )
        conexion.commit()
        return cursor.lastrowid
    finally:
        conexion.close()


def obtener_productos():
    """Devuelve la lista de todos los productos, ordenados por ID."""
    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos ORDER BY id")
        return cursor.fetchall()
    finally:
        conexion.close()


def obtener_producto_por_id(id_producto):
    """Devuelve la fila del producto con ese ID, o None si no existe."""
    conexion = conectar()
    try:
        cursor = conexion.cursor()
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


def actualizar_producto(id_producto, nombre, descripcion, cantidad, precio, categoria):
    """Reemplaza los datos del producto con ese ID."""
    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE productos SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ? "
            "WHERE id = ?",
            (nombre, descripcion, cantidad, precio, categoria, id_producto),
        )
        conexion.commit()
    finally:
        conexion.close()


def eliminar_producto(id_producto):
    """Elimina el producto con ese ID."""
    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        conexion.commit()
    finally:
        conexion.close()


def buscar_productos(campo, texto):
    """
    Devuelve los productos cuyo 'campo' ("nombre" o "categoria") contenga el texto.
    LIKE con % permite coincidencias parciales y no distingue mayúsculas.
    """
    # 'campo' no viene del usuario: solo se aceptan estos dos valores,
    # y el texto del usuario va siempre como parámetro (?), nunca dentro del SQL.
    if campo not in ("nombre", "categoria"):
        raise ValueError(f"Campo de búsqueda inválido: {campo}")

    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            f"SELECT * FROM productos WHERE {campo} LIKE ? ORDER BY id",
            (f"%{texto}%",),
        )
        return cursor.fetchall()
    finally:
        conexion.close()


def obtener_bajo_stock(limite):
    """Devuelve los productos con cantidad menor o igual al límite indicado."""
    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT * FROM productos WHERE cantidad <= ? ORDER BY cantidad, id",
            (limite,),
        )
        return cursor.fetchall()
    finally:
        conexion.close()
