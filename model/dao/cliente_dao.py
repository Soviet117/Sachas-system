from model.dao.conexion import Conexion
from model.entities.cliente import Cliente


class ClienteDAO:
    def __init__(self):
        self.db = Conexion()

    def listar(self):
        cursor = self.db.ejecutar('SELECT * FROM cliente ORDER BY nombre')
        return [Cliente.from_dict(dict(row)) for row in cursor.fetchall()]

    def obtener_por_id(self, id):
        cursor = self.db.ejecutar('SELECT * FROM cliente WHERE id = ?', (id,))
        row = cursor.fetchone()
        return Cliente.from_dict(dict(row)) if row else None

    def insertar(self, cliente):
        cursor = self.db.ejecutar(
            'INSERT INTO cliente (nombre, telefono, email) VALUES (?, ?, ?)',
            (cliente.nombre, cliente.telefono, cliente.email)
        )
        return cursor.lastrowid

    def actualizar(self, cliente):
        self.db.ejecutar(
            'UPDATE cliente SET nombre=?, telefono=?, email=? WHERE id=?',
            (cliente.nombre, cliente.telefono, cliente.email, cliente.id)
        )

    def eliminar(self, id):
        self.db.ejecutar('DELETE FROM cliente WHERE id = ?', (id,))

    def buscar(self, query):
        cursor = self.db.ejecutar(
            'SELECT * FROM cliente WHERE nombre LIKE ? OR telefono LIKE ?',
            (f'%{query}%', f'%{query}%')
        )
        return [Cliente.from_dict(dict(row)) for row in cursor.fetchall()]

    def acumular_puntos(self, id_cliente, puntos):
        self.db.ejecutar('UPDATE cliente SET puntos = puntos + ? WHERE id = ?', (puntos, id_cliente))