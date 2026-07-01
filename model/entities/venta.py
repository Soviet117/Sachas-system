class Venta:
    def __init__(self, id=None, id_pedido=None, total=0.0, metodo_pago='efectivo', fecha=''):
        self.id = id
        self.id_pedido = id_pedido
        self.total = total
        self.metodo_pago = metodo_pago
        self.fecha = fecha

    def to_dict(self):
        return {
            'id': self.id,
            'id_pedido': self.id_pedido,
            'total': self.total,
            'metodo_pago': self.metodo_pago,
            'fecha': self.fecha
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            id_pedido=data.get('id_pedido'),
            total=data.get('total', 0.0),
            metodo_pago=data.get('metodo_pago', 'efectivo'),
            fecha=data.get('fecha', '')
        )