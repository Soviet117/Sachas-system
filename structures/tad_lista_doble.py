class NodoListaDoble:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None


class ListaDoblementeEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self._tamano = 0

    def insertar_inicio(self, dato):
        nodo = NodoListaDoble(dato)
        if self.esta_vacia():
            self.cabeza = nodo
            self.cola = nodo
        else:
            nodo.siguiente = self.cabeza
            self.cabeza.anterior = nodo
            self.cabeza = nodo
        self._tamano += 1

    def insertar_final(self, dato):
        nodo = NodoListaDoble(dato)
        if self.esta_vacia():
            self.cabeza = nodo
            self.cola = nodo
        else:
            nodo.anterior = self.cola
            self.cola.siguiente = nodo
            self.cola = nodo
        self._tamano += 1

    def eliminar(self, dato):
        actual = self.cabeza
        while actual:
            if actual.dato == dato:
                if actual.anterior:
                    actual.anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                if actual.siguiente:
                    actual.siguiente.anterior = actual.anterior
                else:
                    self.cola = actual.anterior
                self._tamano -= 1
                return True
            actual = actual.siguiente
        return False

    def eliminar_primero(self):
        if self.esta_vacia():
            return None
        dato = self.cabeza.dato
        self.cabeza = self.cabeza.siguiente
        if self.cabeza:
            self.cabeza.anterior = None
        else:
            self.cola = None
        self._tamano -= 1
        return dato

    def eliminar_ultimo(self):
        if self.esta_vacia():
            return None
        dato = self.cola.dato
        self.cola = self.cola.anterior
        if self.cola:
            self.cola.siguiente = None
        else:
            self.cabeza = None
        self._tamano -= 1
        return dato

    def buscar(self, dato):
        actual = self.cabeza
        while actual:
            if actual.dato == dato:
                return actual.dato
            actual = actual.siguiente
        return None

    def recorrer_adelante(self):
        resultado = []
        actual = self.cabeza
        while actual:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def recorrer_atras(self):
        resultado = []
        actual = self.cola
        while actual:
            resultado.append(actual.dato)
            actual = actual.anterior
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
        return ' <-> '.join(str(d) for d in self.recorrer_adelante())
