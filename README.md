# Sistema de gestión de aerolínea

Proyecto integrador del módulo 14 de la guía de estructuras de datos en Python. Las pilas y colas se implementan con arreglos fijos y un contador, siguiendo la guía de pilas y colas.

## Ejecutar

Se necesita Python 3. No requiere instalar librerías adicionales.

Abre la carpeta del repositorio en VS Code y ejecuta en la terminal:

```bash
python main.py
```

En Linux o macOS puedes usar `python3 main.py`.

## Organización

| Ruta | Contenido |
| --- | --- |
| `main.py` | Inicio del programa |
| `modelos/` | Pasajero, vuelo y reserva |
| `estructuras/` | Pila, cola, lista enlazada, árbol BST y grafo |
| `servicios/` | Operaciones, validaciones y persistencia |
| `vistas/` | Menús de consola |
| `datos/aerolinea.json` | Datos guardados |
| `LEEME.txt` | Instrucciones y prueba de uso |

## Funciones

- Registrar, consultar, modificar y eliminar pasajeros y vuelos.
- Crear y cancelar reservas con control de asientos.
- Atender una lista de espera por orden de llegada.
- Deshacer cambios con una pila manual.
- Gestionar escalas mediante una lista enlazada.
- Buscar vuelos por ID con un árbol BST.
- Buscar rutas entre ciudades con un grafo y BFS.
- Guardar los datos y el historial en JSON.

El programa comienza sin datos. Los cambios se guardan al realizarlos.

## Comprobación

Se verificaron las estructuras manuales, los menús, las reservas, la espera, deshacer cambios y la recuperación de datos desde JSON.
