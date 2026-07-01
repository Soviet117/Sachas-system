class NodoLista:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self._tamano = 0

    def insertar_inicio(self, dato):
        nodo = NodoLista(dato)
        nodo.siguiente = self.cabeza
        self.cabeza = nodo
        self._tamano += 1

    def insertar_final(self, dato):
        nodo = NodoLista(dato)
        if not self.cabeza:
            self.cabeza = nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nodo
        self._tamano += 1

    def eliminar(self, dato):
        actual = self.cabeza
        previo = None
        while actual:
            if actual.dato == dato:
                if previo:
                    previo.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                self._tamano -= 1
                return True
            previo = actual
            actual = actual.siguiente
        return False

    def buscar(self, dato):
        actual = self.cabeza
        while actual:
            if actual.dato == dato:
                return actual.dato
            actual = actual.siguiente
        return None

    def recorrer(self):
        resultado = []
        actual = self.cabeza
        while actual:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def tamano(self):
        return self._tamano

    def esta_vacia(self):
        return self._tamano == 0

    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual.dato
            actual = actual.siguiente

    def __repr__(self):
        return ' -> '.join(str(d) for d in self.recorrer())