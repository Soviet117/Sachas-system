from model.dao.cliente_dao import ClienteDAO
from model.entities.cliente import Cliente
from structures.tad_grafo import Grafo
from model.dao.venta_dao import VentaDAO
from model.dao.pedido_dao import PedidoDAO


class ClienteController:
    def __init__(self):
        self.dao = ClienteDAO()
        self.venta_dao = VentaDAO()
        self.pedido_dao = PedidoDAO()
        self._grafo_recomendaciones = None

    def listar(self):
        return self.dao.listar()

    def obtener_por_id(self, id):
        return self.dao.obtener_por_id(id)

    def guardar(self, cliente):
        if cliente.id:
            self.dao.actualizar(cliente)
        else:
            cliente.id = self.dao.insertar(cliente)
        return cliente

    def eliminar(self, id):
        self.dao.eliminar(id)

    def buscar(self, query):
        return self.dao.buscar(query)

    def construir_grafo_recomendaciones(self):
        productos_vendidos = self.venta_dao.top_productos(10)
        grafo = Grafo(dirigido=False)
        for nombre, cantidad in productos_vendidos:
            grafo.agregar_vertice(nombre)
        pedidos = self.pedido_dao.listar()
        for pedido in pedidos[:20]:
            detalles = self.pedido_dao.obtener_detalles(pedido.id)
            nombres = [d.producto_nombre for d in detalles]
            for i in range(len(nombres)):
                for j in range(i + 1, len(nombres)):
                    if nombres[i] in grafo._indices and nombres[j] in grafo._indices:
                        if grafo.existe_arista(nombres[i], nombres[j]):
                            pass
                        grafo.agregar_arista(nombres[i], nombres[j], 1)
        self._grafo_recomendaciones = grafo
        return grafo

    def obtener_grafo(self):
        if not self._grafo_recomendaciones:
            return self.construir_grafo_recomendaciones()
        return self._grafo_recomendaciones