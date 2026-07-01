from model.dao.conexion import Conexion
from model.entities.venta import Venta


class VentaDAO:
    def __init__(self):
        self.db = Conexion()

    def listar(self):
        cursor = self.db.ejecutar('SELECT * FROM venta ORDER BY fecha DESC')
        return [Venta.from_dict(dict(row)) for row in cursor.fetchall()]

    def insertar(self, venta):
        cursor = self.db.ejecutar(
            'INSERT INTO venta (id_pedido, total, metodo_pago) VALUES (?, ?, ?)',
            (venta.id_pedido, venta.total, venta.metodo_pago)
        )
        return cursor.lastrowid

    def ventas_del_dia(self):
        cursor = self.db.ejecutar('''
            SELECT COALESCE(SUM(total), 0) as total
            FROM venta
            WHERE date(fecha) = date('now')
        ''')
        row = cursor.fetchone()
        return row['total'] if row else 0.0

    def contar_ventas_del_dia(self):
        cursor = self.db.ejecutar('''
            SELECT COUNT(*) as count
            FROM venta
            WHERE date(fecha) = date('now')
        ''')
        row = cursor.fetchone()
        return row['count'] if row else 0

    def top_productos(self, limite=5):
        cursor = self.db.ejecutar('''
            SELECT pr.nombre, SUM(dp.cantidad) as total_vendido
            FROM detalle_pedido dp
            JOIN pedido p ON dp.id_pedido = p.id
            JOIN venta v ON p.id = v.id_pedido
            JOIN producto pr ON dp.id_producto = pr.id
            WHERE date(v.fecha) = date('now')
            GROUP BY pr.id
            ORDER BY total_vendido DESC
            LIMIT ?
        ''', (limite,))
        return [(row['nombre'], row['total_vendido']) for row in cursor.fetchall()]