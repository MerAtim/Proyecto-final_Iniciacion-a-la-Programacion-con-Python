# Módulo de conexión a la base de datos SQLite 'inventario.db'.

import os
import sqlite3

# La base de datos se crea en la misma carpeta que este archivo
RUTA_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventario.db")


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
