Sachas Café - Sistema de Gestión
==================================

Este proyecto es un sistema de gestión integral para la cafetería Sachas,
desarrollado como parte del curso de **Algoritmos y Estructuras de Datos**
de la universidad. Implementa en un solo sistema funcional todos los
TADs y estructuras de datos vistos en el sílabo.

¿Por qué Sachas?
----------------

Sachas evoca la calidez y el aroma del café peruano de especialidad.
El nombre busca rendir homenaje a la tradición cafetalera del Perú,
fusionando la tecnología con el arte de preparar un buen café. Este
sistema demuestra que las estructuras de datos no son solo teoría —
están presentes en cada pedido, en cada recomendación y en cada
transacción de una cafetería real.

Arquitectura
------------

El proyecto utiliza un patrón **MVC + DAO** híbrido:

* **Model (DAO)** → Capa de acceso a datos con SQLite mediante el
  patrón Data Access Object.
* **View** → Interfaz gráfica con CustomTkinter (tema oscuro, diseño
  tipo web, sidebar de navegación).
* **Controller** → Lógica de negocio que orquesta las operaciones.
* **Structures** → Implementaciones puras en Python de las estructuras
  del curso (lista enlazada, pila, cola, árbol AVL, grafo).

Estructuras de Datos Implementadas
-----------------------------------

| Estructura | Uso en el sistema | Unidad del sílabo |
|---|---|---|
| **TAD (clases)** | Producto, Pedido, Cliente, Venta | Unidad I |
| **Arreglos** | Productos del día, top ventas | Unidad II |
| **Lista enlazada** | Pedidos pendientes por mesa | Unidad II |
| **Pila (Stack)** | Deshacer acciones en caja (LIFO) | Unidad II |
| **Cola (Queue)** | Cola FIFO de pedidos a cocina | Unidad II |
| **Grafo** | Recomendación de combos (matriz adyacencia) | Unidad III |
| **Árbol AVL** | Catálogo de productos auto-balanceado | Unidad IV |

Módulos del Sistema
-------------------

* **Dashboard** — KPIs del día (ventas, pedidos en cola, top productos)
* **Menú** — CRUD de productos con visualización del árbol AVL
* **Pedidos** — Cola FIFO, preparación y deshacer (pila)
* **Caja** — Punto de venta con resumen de caja
* **Clientes** — CRUD con grafo de recomendaciones
* **Estructuras** — Visualizador interactivo de estructuras

Clonar y Ejecutar
-----------------

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/sachas-cafe.git
cd sachas-cafe

# 2. Instalar dependencia del sistema (solo Linux — tkinter no viene con Python)
# En Ubuntu/Debian:
sudo apt install python3-tk
# En Fedora:
# sudo dnf install python3-tkinter
# En Arch:
# sudo pacman -S tk


# 3. Crear y activar entorno virtual (opcional pero recomendado)
python3 -m venv .venv
source .venv/bin/activate    # Linux / macOS
# .venv\Scripts\activate     # Windows

# 4. Instalar dependencias Python
pip install -r requirements.txt

# 5. Ejecutar el sistema
python main.py
```

La base de datos se crea automáticamente en la primera ejecución
con 15 productos y 3 clientes de ejemplo.
