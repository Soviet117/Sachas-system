from model.dao.conexion import Conexion
from model.entities.producto import Producto


class ProductoDAO:
    def __init__(self):
        self.db = Conexion()

    def listar(self):
        cursor = self.db.ejecutar('SELECT * FROM producto ORDER BY categoria, nombre')
        return [Producto.from_dict(dict(row)) for row in cursor.fetchall()]

    def obtener_por_id(self, id):
        cursor = self.db.ejecutar('SELECT * FROM producto WHERE id = ?', (id,))
        row = cursor.fetchone()
        return Producto.from_dict(dict(row)) if row else None

    def insertar(self, producto):
        cursor = self.db.ejecutar(
            'INSERT INTO producto (nombre, descripcion, precio, categoria, stock) VALUES (?, ?, ?, ?, ?)',
            (producto.nombre, producto.descripcion, producto.precio, producto.categoria, producto.stock)
        )
        return cursor.lastrowid

    def actualizar(self, producto):
        self.db.ejecutar(
            'UPDATE producto SET nombre=?, descripcion=?, precio=?, categoria=?, stock=? WHERE id=?',
            (producto.nombre, producto.descripcion, producto.precio, producto.categoria, producto.stock, producto.id)
        )

    def eliminar(self, id):
        self.db.ejecutar('DELETE FROM producto WHERE id = ?', (id,))

    def buscar(self, query):
        cursor = self.db.ejecutar(
            'SELECT * FROM producto WHERE nombre LIKE ? OR categoria LIKE ?',
            (f'%{query}%', f'%{query}%')
        )
        return [Producto.from_dict(dict(row)) for row in cursor.fetchall()]

    def listar_categorias(self):
        cursor = self.db.ejecutar('SELECT DISTINCT categoria FROM producto ORDER BY categoria')
        return [row['categoria'] for row in cursor.fetchall()]