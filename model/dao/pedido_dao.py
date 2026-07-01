from model.dao.conexion import Conexion
from model.entities.pedido import Pedido, DetallePedido


class PedidoDAO:
    def __init__(self):
        self.db = Conexion()

    def listar(self):
        cursor = self.db.ejecutar('''
            SELECT p.*, COALESCE(c.nombre, 'General') as cliente_nombre
            FROM pedido p
            LEFT JOIN cliente c ON p.id_cliente = c.id
            ORDER BY p.fecha DESC
        ''')
        return [Pedido.from_dict(dict(row)) for row in cursor.fetchall()]

    def listar_por_estado(self, estado):
        cursor = self.db.ejecutar('''
            SELECT p.*, COALESCE(c.nombre, 'General') as cliente_nombre
            FROM pedido p
            LEFT JOIN cliente c ON p.id_cliente = c.id
            WHERE p.estado = ?
            ORDER BY p.fecha ASC
        ''', (estado,))
        return [Pedido.from_dict(dict(row)) for row in cursor.fetchall()]

    def obtener_por_id(self, id):
        cursor = self.db.ejecutar('''
            SELECT p.*, COALESCE(c.nombre, 'General') as cliente_nombre
            FROM pedido p
            LEFT JOIN cliente c ON p.id_cliente = c.id
            WHERE p.id = ?
        ''', (id,))
        row = cursor.fetchone()
        if not row:
            return None
        pedido = Pedido.from_dict(dict(row))
        pedido.detalles = self.obtener_detalles(id)
        return pedido

    def insertar(self, pedido):
        cursor = self.db.ejecutar(
            'INSERT INTO pedido (id_cliente, estado, total) VALUES (?, ?, ?)',
            (pedido.id_cliente, pedido.estado, pedido.total)
        )
        return cursor.lastrowid

    def actualizar_estado(self, id, estado):
        self.db.ejecutar('UPDATE pedido SET estado = ? WHERE id = ?', (estado, id))

    def obtener_detalles(self, id_pedido):
        cursor = self.db.ejecutar('''
            SELECT d.*, pr.nombre as producto_nombre
            FROM detalle_pedido d
            JOIN producto pr ON d.id_producto = pr.id
            WHERE d.id_pedido = ?
        ''', (id_pedido,))
        return [DetallePedido(
            id=row['id'], id_pedido=row['id_pedido'],
            id_producto=row['id_producto'], cantidad=row['cantidad'],
            subtotal=row['subtotal'], producto_nombre=row['producto_nombre']
        ) for row in cursor.fetchall()]

    def insertar_detalle(self, detalle):
        self.db.ejecutar(
            'INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad, subtotal) VALUES (?, ?, ?, ?)',
            (detalle.id_pedido, detalle.id_producto, detalle.cantidad, detalle.subtotal)
        )