<div align="center">

<h1>
  TRABAJO FINAL INTEGRADOR&nbsp;&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="60" style="position: relative; top: 6 px; margin-left: 10 px;">
</h1>

<h3>Sistema de gestión de inventario</h3>
<br>
</div>

## Descripción

Aplicación de consola en Python para administrar el inventario de productos
de un comercio. Los datos se guardan en una base de datos SQLite llamada
'inventario.db', que se crea automáticamente junto a tfi.py la primera vez
que se ejecuta el programa.
<br>

## Requisitos

- Python 3
- (Opcional) colorama, para ver los mensajes con colores:
      pip install colorama
  Si no está instalado, el programa funciona igual, sin colores.
<br>

## Ejecución
    python tfi.py
<br>

## Funcionalidades del menú

1. Registrar producto       -> nombre, descripción, cantidad, precio y categoría.
2. Visualizar productos     -> lista todos los productos en forma de tabla.
3. Actualizar producto      -> por ID; Enter conserva el valor actual de cada campo.
4. Eliminar producto        -> por ID, con confirmación previa.
5. Buscar producto          -> por ID, por nombre o por categoría (búsqueda parcial).
6. Reporte de bajo stock    -> productos con cantidad igual o menor a un límite. 
7. Salir <br>

## Estructura de la tabla 'productos'

| Campo       | Tipo    | Restricciones                      |
|------------|---------|------------------------------------|
| id         | INTEGER | Clave primaria, autoincremental    |
| nombre     | TEXT    | No nulo                            |
| descripcion| TEXT    | -                                  |
| cantidad   | INTEGER | No nulo, >= 0                      |
| precio     | REAL    | No nulo, >= 0                      |
| categoria  | TEXT    | -                                  |

<br>

## Buenas prácticas aplicadas

- Código dividido en funciones (base de datos, validaciones, presentación, CRUD, menú).
- Consultas parametrizadas (?) para prevenir inyecciones SQL.
- Manejo de errores con try-except y cierre de la conexión con finally.
- Validación de todos los datos ingresados antes de guardarlos
  (nombre y categoría deben tener letras; no se permiten nombres de producto repetidos).

<br>

## Capturas:

### Agregar producto:
<img width="471" height="584" alt="image" src="https://github.com/user-attachments/assets/7e0cfb9e-8fc0-49c9-8906-f0b2e98c4b78" />

<br>

### Excepciones: nombre no puede quedar vacío, ni acepta signos ni números solos:
<img width="563" height="471" alt="image" src="https://github.com/user-attachments/assets/32b60953-e332-4830-b7bf-b5ff6ead94b7" />

<br>

### Ver productos:
<img width="760" height="394" alt="image" src="https://github.com/user-attachments/assets/a8768f86-b96b-4114-be5b-ae256073b8b8" />

<br>

### Actualizar un producto:

<img width="790" height="875" alt="image" src="https://github.com/user-attachments/assets/cdd5f4fb-1233-4aa9-81b1-fffbb1183411" />

<br>

### Eliminar producto:

<img width="475" height="437" alt="image" src="https://github.com/user-attachments/assets/b79bea43-ff64-45c1-876e-8b33427bd852" />

<br>

### Buscar Producto:

<img width="329" height="464" alt="image" src="https://github.com/user-attachments/assets/9e8632a8-a66b-4374-a620-51248d6df3fc" />

<br>

### Reporte de bajo stock:

<img width="435" height="289" alt="image" src="https://github.com/user-attachments/assets/479d7562-2eb2-44a8-9902-13fe3f3b4618" />
