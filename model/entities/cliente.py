class Cliente:
    def __init__(self, id=None, nombre='', telefono='', email='', puntos=0):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.puntos = puntos

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'email': self.email,
            'puntos': self.puntos
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            nombre=data.get('nombre', ''),
            telefono=data.get('telefono', ''),
            email=data.get('email', ''),
            puntos=data.get('puntos', 0)
        )

    def __repr__(self):
        return f'Cliente({self.id}, {self.nombre})'