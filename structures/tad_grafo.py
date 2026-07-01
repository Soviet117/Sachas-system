class Grafo:
    def __init__(self, dirigido=False):
        self.dirigido = dirigido
        self._vertices = []
        self._matriz = []
        self._indices = {}

    def agregar_vertice(self, vertice):
        if vertice not in self._indices:
            self._indices[vertice] = len(self._vertices)
            self._vertices.append(vertice)
            for fila in self._matriz:
                fila.append(0)
            self._matriz.append([0] * len(self._vertices))

    def agregar_arista(self, origen, destino, peso=1):
        if origen not in self._indices:
            self.agregar_vertice(origen)
        if destino not in self._indices:
            self.agregar_vertice(destino)
        i, j = self._indices[origen], self._indices[destino]
        self._matriz[i][j] = peso
        if not self.dirigido:
            self._matriz[j][i] = peso

    def eliminar_arista(self, origen, destino):
        if origen in self._indices and destino in self._indices:
            i, j = self._indices[origen], self._indices[destino]
            self._matriz[i][j] = 0
            if not self.dirigido:
                self._matriz[j][i] = 0

    def eliminar_vertice(self, vertice):
        if vertice not in self._indices:
            return
        idx = self._indices[vertice]
        self._vertices.pop(idx)
        self._matriz.pop(idx)
        for fila in self._matriz:
            fila.pop(idx)
        self._indices.clear()
        for i, v in enumerate(self._vertices):
            self._indices[v] = i

    def obtener_matriz(self):
        return self._matriz

    def obtener_vertices(self):
        return self._vertices

    def adyacentes(self, vertice):
        if vertice not in self._indices:
            return []
        idx = self._indices[vertice]
        return [
            self._vertices[j]
            for j, peso in enumerate(self._matriz[idx])
            if peso != 0
        ]

    def existe_arista(self, origen, destino):
        if origen in self._indices and destino in self._indices:
            return self._matriz[self._indices[origen]][self._indices[destino]] != 0
        return False

    def bfs(self, inicio):
        if inicio not in self._indices:
            return []
        visitados = set()
        cola = [inicio]
        recorrido = []
        while cola:
            vertice = cola.pop(0)
            if vertice not in visitados:
                visitados.add(vertice)
                recorrido.append(vertice)
                for ady in self.adyacentes(vertice):
                    if ady not in visitados:
                        cola.append(ady)
        return recorrido

    def dfs(self, inicio):
        if inicio not in self._indices:
            return []
        visitados = set()
        pila = [inicio]
        recorrido = []
        while pila:
            vertice = pila.pop()
            if vertice not in visitados:
                visitados.add(vertice)
                recorrido.append(vertice)
                for ady in self.adyacentes(vertice):
                    if ady not in visitados:
                        pila.append(ady)
        return recorrido

    def warshall(self):
        n = len(self._vertices)
        C = [fila[:] for fila in self._matriz]
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    C[i][j] = C[i][j] or (C[i][k] and C[k][j])
        return C

    def es_euleriano(self):
        if self.dirigido:
            return False
        impares = sum(
            1 for v in self._vertices
            if len(self.adyacentes(v)) % 2 != 0
        )
        return impares == 0

    def es_hamiltoniano(self):
        n = len(self._vertices)
        if n == 0:
            return False
        visitados = set()

        def backtrack(v, count):
            if count == n:
                return True
            for w in self.adyacentes(v):
                if w not in visitados:
                    visitados.add(w)
                    if backtrack(w, count + 1):
                        return True
                    visitados.remove(w)
            return False

        for v in self._vertices:
            visitados.add(v)
            if backtrack(v, 1):
                return True
            visitados.remove(v)
        return False

    def __repr__(self):
        txt = f'Grafo {"dirigido" if self.dirigido else "no dirigido"}\n'
        txt += 'Matriz de Adyacencia:\n   ' + ' '.join(f'{v:>8}' for v in self._vertices) + '\n'
        for i, v in enumerate(self._vertices):
            txt += f'{v:>3} ' + ' '.join(f'{self._matriz[i][j]:>8}' for j in range(len(self._vertices))) + '\n'
        return txt