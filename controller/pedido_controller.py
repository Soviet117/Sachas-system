from model.dao.pedido_dao import PedidoDAO
from model.dao.venta_dao import VentaDAO
from model.dao.cliente_dao import ClienteDAO
from model.entities.pedido import Pedido, DetallePedido
from model.entities.venta import Venta
from structures.tad_cola import Cola
from structures.tad_pila import Pila
from structures.tad_lista import ListaEnlazada


class PedidoController:
    def __init__(self):
        self.dao = PedidoDAO()
        self.venta_dao = VentaDAO()
        self.cliente_dao = ClienteDAO()
        self.cola_pedidos = Cola()
        self.pila_deshacer = Pila()
        self.lista_pendientes = ListaEnlazada()
        self._cargar_cola()

    def _cargar_cola(self):
        pedidos = self.dao.listar_por_estado('en_cola')
        for p in pedidos:
            self.cola_pedidos.enqueue(p)
        pendientes = self.dao.listar_por_estado('preparacion')
        for p in pendientes:
            self.lista_pendientes.insertar_final(p)

    def crear_pedido(self, id_cliente, items):
        total = sum(item['subtotal'] for item in items)
        pedido = Pedido(id_cliente=id_cliente, total=total)
        pedido.id = self.dao.insertar(pedido)
        for item in items:
            detalle = DetallePedido(
                id_pedido=pedido.id,
                id_producto=item['id_producto'],
                cantidad=item['cantidad'],
                subtotal=item['subtotal']
            )
            self.dao.insertar_detalle(detalle)
        pedido.detalles = self.dao.obtener_detalles(pedido.id)
        pedido.cliente_nombre = 'General'
        self.cola_pedidos.enqueue(pedido)
        self.pila_deshacer.push(('crear', pedido.id))
        return pedido

    def siguiente_en_cola(self):
        return self.cola_pedidos.peek()

    def pasar_a_preparacion(self):
        pedido = self.cola_pedidos.dequeue()
        if pedido:
            self.dao.actualizar_estado(pedido.id, 'preparacion')
            pedido.estado = 'preparacion'
            self.lista_pendientes.insertar_final(pedido)
            self.pila_deshacer.push(('preparar', pedido.id))
        return pedido

    def marcar_listo(self, id_pedido):
        self.dao.actualizar_estado(id_pedido, 'listo')
        pedido = self.dao.obtener_por_id(id_pedido)
        nodo = self.lista_pendientes.cabeza
        while nodo:
            if nodo.dato.id == id_pedido:
                nodo.dato.estado = 'listo'
                break
            nodo = nodo.siguiente
        self.pila_deshacer.push(('listo', id_pedido))
        return pedido

    def cobrar_pedido(self, id_pedido, metodo_pago='efectivo'):
        pedido = self.dao.obtener_por_id(id_pedido)
        venta = Venta(id_pedido=id_pedido, total=pedido.total, metodo_pago=metodo_pago)
        self.venta_dao.insertar(venta)
        self.dao.actualizar_estado(id_pedido, 'completado')
        if pedido.id_cliente:
            self.cliente_dao.acumular_puntos(pedido.id_cliente, int(pedido.total))
        return venta

    def deshacer_ultima_accion(self):
        accion = self.pila_deshacer.pop()
        if not accion:
            return None
        tipo, id_pedido = accion
        if tipo == 'crear':
            self.dao.actualizar_estado(id_pedido, 'cancelado')
            return f'Pedido #{id_pedido} cancelado'
        elif tipo == 'preparar':
            self.dao.actualizar_estado(id_pedido, 'en_cola')
            pedido = self.dao.obtener_por_id(id_pedido)
            if pedido:
                self.cola_pedidos.enqueue(pedido)
            return f'Pedido #{id_pedido} devuelto a la cola'
        elif tipo == 'listo':
            self.dao.actualizar_estado(id_pedido, 'preparacion')
            return f'Pedido #{id_pedido} devuelto a preparación'
        return None

    def obtener_cola(self):
        return self.cola_pedidos.recorrer()

    def obtener_pendientes(self):
        return [n.dato for n in self.lista_pendientes if n.dato.estado == 'preparacion']

    def obtener_pila_deshacer(self):
        return self.pila_deshacer.recorrer()

    def obtener_pedidos_recientes(self, limite=5):
        return self.dao.listar()[:limite]