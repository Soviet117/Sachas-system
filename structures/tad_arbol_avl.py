class NodoAVL:
    def __init__(self, clave, valor=None):
        self.clave = clave
        self.valor = valor
        self.altura = 1
        self.izquierdo = None
        self.derecho = None


class ArbolAVL:
    def __init__(self):
        self.raiz = None
        self._operaciones = []

    def _altura(self, nodo):
        return nodo.altura if nodo else 0

    def _balance(self, nodo):
        return self._altura(nodo.izquierdo) - self._altura(nodo.derecho) if nodo else 0

    def _actualizar_altura(self, nodo):
        if nodo:
            nodo.altura = 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))

    def _rotacion_derecha(self, y):
        x = y.izquierdo
        T2 = x.derecho
        x.derecho = y
        y.izquierdo = T2
        self._actualizar_altura(y)
        self._actualizar_altura(x)
        self._operaciones.append(f'Rotación Simple Derecha ({y.clave})')
        return x

    def _rotacion_izquierda(self, x):
        y = x.derecho
        T2 = y.izquierdo
        y.izquierdo = x
        x.derecho = T2
        self._actualizar_altura(x)
        self._actualizar_altura(y)
        self._operaciones.append(f'Rotación Simple Izquierda ({x.clave})')
        return y

    def insertar(self, clave, valor=None):
        self._operaciones.append(f'Insertar: {clave}')
        self.raiz = self._insertar_rec(self.raiz, clave, valor)

    def _insertar_rec(self, nodo, clave, valor):
        if not nodo:
            return NodoAVL(clave, valor)
        if clave < nodo.clave:
            nodo.izquierdo = self._insertar_rec(nodo.izquierdo, clave, valor)
        elif clave > nodo.clave:
            nodo.derecho = self._insertar_rec(nodo.derecho, clave, valor)
        else:
            nodo.valor = valor
            return nodo

        self._actualizar_altura(nodo)
        balance = self._balance(nodo)

        if balance > 1 and clave < nodo.izquierdo.clave:
            self._operaciones.append(f'Rotación Derecha en {nodo.clave}')
            return self._rotacion_derecha(nodo)
        if balance < -1 and clave > nodo.derecho.clave:
            self._operaciones.append(f'Rotación Izquierda en {nodo.clave}')
            return self._rotacion_izquierda(nodo)
        if balance > 1 and clave > nodo.izquierdo.clave:
            self._operaciones.append(f'Rotación Doble (Izq-Der) en {nodo.clave}')
            nodo.izquierdo = self._rotacion_izquierda(nodo.izquierdo)
            return self._rotacion_derecha(nodo)
        if balance < -1 and clave < nodo.derecho.clave:
            self._operaciones.append(f'Rotación Doble (Der-Izq) en {nodo.clave}')
            nodo.derecho = self._rotacion_derecha(nodo.derecho)
            return self._rotacion_izquierda(nodo)

        return nodo

    def buscar(self, clave):
        return self._buscar_rec(self.raiz, clave)

    def _buscar_rec(self, nodo, clave):
        if not nodo or nodo.clave == clave:
            return nodo
        if clave < nodo.clave:
            return self._buscar_rec(nodo.izquierdo, clave)
        return self._buscar_rec(nodo.derecho, clave)

    def eliminar(self, clave):
        self._operaciones.append(f'Eliminar: {clave}')
        self.raiz = self._eliminar_rec(self.raiz, clave)

    def _eliminar_rec(self, nodo, clave):
        if not nodo:
            return None
        if clave < nodo.clave:
            nodo.izquierdo = self._eliminar_rec(nodo.izquierdo, clave)
        elif clave > nodo.clave:
            nodo.derecho = self._eliminar_rec(nodo.derecho, clave)
        else:
            if not nodo.izquierdo:
                return nodo.derecho
            if not nodo.derecho:
                return nodo.izquierdo
            sucesor = self._min(nodo.derecho)
            nodo.clave = sucesor.clave
            nodo.valor = sucesor.valor
            nodo.derecho = self._eliminar_rec(nodo.derecho, sucesor.clave)

        self._actualizar_altura(nodo)
        balance = self._balance(nodo)

        if balance > 1 and self._balance(nodo.izquierdo) >= 0:
            return self._rotacion_derecha(nodo)
        if balance > 1 and self._balance(nodo.izquierdo) < 0:
            nodo.izquierdo = self._rotacion_izquierda(nodo.izquierdo)
            return self._rotacion_derecha(nodo)
        if balance < -1 and self._balance(nodo.derecho) <= 0:
            return self._rotacion_izquierda(nodo)
        if balance < -1 and self._balance(nodo.derecho) > 0:
            nodo.derecho = self._rotacion_derecha(nodo.derecho)
            return self._rotacion_izquierda(nodo)

        return nodo

    def _min(self, nodo):
        while nodo.izquierdo:
            nodo = nodo.izquierdo
        return nodo

    def inorden(self):
        resultado = []
        self._inorden_rec(self.raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo, resultado):
        if nodo:
            self._inorden_rec(nodo.izquierdo, resultado)
            resultado.append((nodo.clave, nodo.valor))
            self._inorden_rec(nodo.derecho, resultado)

    def preorden(self):
        resultado = []
        self._preorden_rec(self.raiz, resultado)
        return resultado

    def _preorden_rec(self, nodo, resultado):
        if nodo:
            resultado.append((nodo.clave, nodo.valor))
            self._preorden_rec(nodo.izquierdo, resultado)
            self._preorden_rec(nodo.derecho, resultado)

    def postorden(self):
        resultado = []
        self._postorden_rec(self.raiz, resultado)
        return resultado

    def _postorden_rec(self, nodo, resultado):
        if nodo:
            self._postorden_rec(nodo.izquierdo, resultado)
            self._postorden_rec(nodo.derecho, resultado)
            resultado.append((nodo.clave, nodo.valor))

    def obtener_operaciones(self):
        ops = self._operaciones[:]
        self._operaciones.clear()
        return ops

    def obtener_niveles(self):
        niveles = []
        self._niveles_rec(self.raiz, 0, niveles)
        return niveles

    def _niveles_rec(self, nodo, nivel, niveles):
        if nodo:
            if len(niveles) <= nivel:
                niveles.append([])
            niveles[nivel].append((nodo.clave, nodo.valor))
            self._niveles_rec(nodo.izquierdo, nivel + 1, niveles)
            self._niveles_rec(nodo.derecho, nivel + 1, niveles)