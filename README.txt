TRABAJO FINAL INTEGRADOR - Sistema de gestión de inventario
============================================================

Descripción
-----------
Aplicación de consola en Python para administrar el inventario de productos
de un comercio. Los datos se guardan en una base de datos SQLite llamada
'inventario.db', que se crea automáticamente junto a tfi.py la primera vez
que se ejecuta el programa.

Requisitos
----------
- Python 3
- (Opcional) colorama, para ver los mensajes con colores:
      pip install colorama
  Si no está instalado, el programa funciona igual, sin colores.

Ejecución
---------
    python tfi.py

Funcionalidades del menú
------------------------
1. Registrar producto       -> nombre, descripción, cantidad, precio y categoría.
2. Visualizar productos     -> lista todos los productos en forma de tabla.
3. Actualizar producto      -> por ID; Enter conserva el valor actual de cada campo.
4. Eliminar producto        -> por ID, con confirmación previa.
5. Buscar producto          -> por ID, por nombre o por categoría (búsqueda parcial).
6. Reporte de bajo stock    -> productos con cantidad igual o menor a un límite.
7. Salir

Estructura de la tabla 'productos'
----------------------------------
id           INTEGER  clave primaria, autoincremental
nombre       TEXT     no nulo
descripcion  TEXT
cantidad     INTEGER  no nulo, >= 0
precio       REAL     no nulo, >= 0
categoria    TEXT

Buenas prácticas aplicadas
--------------------------
- Código dividido en funciones (base de datos, validaciones, presentación, CRUD, menú).
- Consultas parametrizadas (?) para prevenir inyecciones SQL.
- Manejo de errores con try-except y cierre de la conexión con finally.
- Validación de todos los datos ingresados antes de guardarlos
  (nombre y categoría deben tener letras; no se permiten nombres de producto repetidos).
