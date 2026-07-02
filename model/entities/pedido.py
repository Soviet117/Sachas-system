class DetallePedido:
    def __init__(self, id=None, id_pedido=None, id_producto=None, cantidad=1, subtotal=0.0, producto_nombre=''):
        self.id = id
        self.id_pedido = id_pedido
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.subtotal = subtotal
        self.producto_nombre = producto_nombre

    def to_dict(self):
        return {
            'id': self.id,
            'id_pedido': self.id_pedido,
            'id_producto': self.id_producto,
            'cantidad': self.cantidad,
            'subtotal': self.subtotal,
            'producto_nombre': self.producto_nombre
        }


class Pedido:
    def __init__(self, id=None, id_cliente=None, fecha='', estado='en_cola', total=0.0, cliente_nombre=''):
        self.id = id
        self.id_cliente = id_cliente
        self.fecha = fecha
        self.estado = estado
        self.total = total
        self.cliente_nombre = cliente_nombre
        self.detalles = []

    def to_dict(self):
        return {
            'id': self.id,
            'id_cliente': self.id_cliente,
            'fecha': self.fecha,
            'estado': self.estado,
            'total': self.total,
            'cliente_nombre': self.cliente_nombre,
            'detalles': [d.to_dict() for d in self.detalles]
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            id_cliente=data.get('id_cliente'),
            fecha=data.get('fecha', ''),
            estado=data.get('estado', 'en_cola'),
            total=data.get('total', 0.0),
            cliente_nombre=data.get('cliente_nombre', '')
        )

    def __eq__(self, other):
        if isinstance(other, Pedido):
            return self.id == other.id
        return NotImplemented

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f'Pedido({self.id}, {self.estado}, S/{self.total:.2f})'