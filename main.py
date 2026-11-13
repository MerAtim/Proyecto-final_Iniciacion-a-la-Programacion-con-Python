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
#
# Estructura del proyecto:
# - main.py          -> punto de entrada y menú principal
# - funciones.py     -> interacción con el usuario (entradas, mensajes, opciones del menú)
# - funciones_sql.py -> consultas a la base de datos
# - conexion.py      -> conexión a la base de datos y creación de la tabla

import sqlite3

from conexion import crear_tabla
from funciones import (
    Fore,
    Style,
    mensaje_error,
    mensaje_exito,
    registrar_producto,
    visualizar_productos,
    actualizar_producto,
    eliminar_producto,
    buscar_producto,
    reporte_bajo_stock,
)


def mostrar_menu():
    print("\n" + Fore.CYAN + Style.BRIGHT + "---------------------------------------")
    print(Fore.CYAN + Style.BRIGHT + "   Sistema de gestión de inventario")
    print(Fore.CYAN + Style.BRIGHT + "---------------------------------------")
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
