class NodoCola:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Cola:
    def __init__(self):
        self._frente = None
        self._final = None
        self._tamano = 0

    def enqueue(self, dato):
        nodo = NodoCola(dato)
        if self.esta_vacia():
            self._frente = nodo
            self._final = nodo
        else:
            self._final.siguiente = nodo
            self._final = nodo
        self._tamano += 1

    def dequeue(self):
        if self.esta_vacia():
            return None
        dato = self._frente.dato
        self._frente = self._frente.siguiente
        if not self._frente:
            self._final = None
        self._tamano -= 1
        return dato

    def peek(self):
        if self.esta_vacia():
            return None
        return self._frente.dato

    def esta_vacia(self):
        return self._frente is None

    def tamano(self):
        return self._tamano

    def recorrer(self):
        resultado = []
        actual = self._frente
        while actual:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def vaciar(self):
        self._frente = None
        self._final = None
        self._tamano = 0

    def __repr__(self):
        return ' -> '.join(str(d) for d in self.recorrer())