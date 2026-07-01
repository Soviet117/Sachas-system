from model.dao.producto_dao import ProductoDAO
from model.entities.producto import Producto
from structures.tad_arbol_avl import ArbolAVL


class ProductoController:
    def __init__(self):
        self.dao = ProductoDAO()
        self._arbol_catalogo = None

    def listar(self):
        return self.dao.listar()

    def obtener_por_id(self, id):
        return self.dao.obtener_por_id(id)

    def guardar(self, producto):
        if producto.id:
            self.dao.actualizar(producto)
        else:
            producto.id = self.dao.insertar(producto)
        return producto

    def eliminar(self, id):
        self.dao.eliminar(id)

    def buscar(self, query):
        return self.dao.buscar(query)

    def listar_categorias(self):
        return self.dao.listar_categorias()

    def construir_arbol_catalogo(self):
        productos = self.dao.listar()
        arbol = ArbolAVL()
        for p in productos:
            arbol.insertar(p.nombre, p)
        self._arbol_catalogo = arbol
        return arbol

    def obtener_arbol(self):
        if not self._arbol_catalogo:
            return self.construir_arbol_catalogo()
        return self._arbol_catalogo