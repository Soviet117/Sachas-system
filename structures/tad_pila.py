class NodoPila:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Pila:
    def __init__(self):
        self._cima = None
        self._tamano = 0

    def push(self, dato):
        nodo = NodoPila(dato)
        nodo.siguiente = self._cima
        self._cima = nodo
        self._tamano += 1

    def pop(self):
        if self.esta_vacia():
            return None
        dato = self._cima.dato
        self._cima = self._cima.siguiente
        self._tamano -= 1
        return dato

    def peek(self):
        if self.esta_vacia():
            return None
        return self._cima.dato

    def esta_vacia(self):
        return self._cima is None

    def tamano(self):
        return self._tamano

    def recorrer(self):
        resultado = []
        actual = self._cima
        while actual:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def vaciar(self):
        self._cima = None
        self._tamano = 0

    def __repr__(self):
        return ' -> '.join(str(d) for d in self.recorrer())