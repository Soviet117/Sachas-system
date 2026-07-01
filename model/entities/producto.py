class Producto:
    def __init__(self, id=None, nombre='', descripcion='', precio=0.0, categoria='', stock=0):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.categoria = categoria
        self.stock = stock

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'categoria': self.categoria,
            'stock': self.stock
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            nombre=data.get('nombre', ''),
            descripcion=data.get('descripcion', ''),
            precio=data.get('precio', 0.0),
            categoria=data.get('categoria', ''),
            stock=data.get('stock', 0)
        )

    def __repr__(self):
        return f'Producto({self.id}, {self.nombre}, S/{self.precio:.2f})'