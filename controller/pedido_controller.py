import time
from model.dao.pedido_dao import PedidoDAO
from model.dao.venta_dao import VentaDAO
from model.dao.cliente_dao import ClienteDAO
from model.entities.pedido import Pedido, DetallePedido
from model.entities.venta import Venta
from model.entities.cliente import Cliente
from structures.tad_cola import Cola
from structures.tad_pila import Pila
from structures.tad_lista_doble import ListaDoblementeEnlazada


class PedidoController:
    def __init__(self):
        self.dao = PedidoDAO()
        self.venta_dao = VentaDAO()
        self.cliente_dao = ClienteDAO()
        self.cola_pedidos = Cola()
        self.cola_espera = Cola()
        self.pila_deshacer = Pila()
        self.lista_pendientes = ListaDoblementeEnlazada()
        self._inicio_preparacion = {}
        self._cargar_colas()

    def _cargar_colas(self):
        for p in self.dao.listar_por_estado('en_cola'):
            p.detalles = self.dao.obtener_detalles(p.id)
            self.cola_pedidos.enqueue(p)
        for p in self.dao.listar_por_estado('espera'):
            p.detalles = self.dao.obtener_detalles(p.id)
            self.cola_espera.enqueue(p)
        for p in self.dao.listar_por_estado('preparacion'):
            p.detalles = self.dao.obtener_detalles(p.id)
            self.lista_pendientes.insertar_final(p)
            self._inicio_preparacion[p.id] = time.time()

    def _cargar_detalles(self, pedido):
        if not pedido.detalles:
            pedido.detalles = self.dao.obtener_detalles(pedido.id)
        return pedido

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
        cliente = self.cliente_dao.obtener_por_id(id_cliente) if id_cliente else None
        pedido.cliente_nombre = cliente.nombre if cliente else 'General'
        self.cola_pedidos.enqueue(pedido)
        self.pila_deshacer.push(('crear', pedido.id))
        return pedido

    def _dequeue_valid(self, cola, estado_esperado):
        while not cola.esta_vacia():
            pedido = cola.dequeue()
            if pedido.estado == estado_esperado:
                return pedido
        return None

    def pasar_a_espera(self):
        pedido = self._dequeue_valid(self.cola_pedidos, 'en_cola')
        if pedido:
            self.dao.actualizar_estado(pedido.id, 'espera')
            pedido.estado = 'espera'
            self._cargar_detalles(pedido)
            self.cola_espera.enqueue(pedido)
            self.pila_deshacer.push(('espera', pedido.id))
        return pedido

    def pasar_a_preparacion(self):
        pedido = self._dequeue_valid(self.cola_espera, 'espera')
        if pedido:
            self.dao.actualizar_estado(pedido.id, 'preparacion')
            pedido.estado = 'preparacion'
            self._cargar_detalles(pedido)
            self.lista_pendientes.insertar_final(pedido)
            self._inicio_preparacion[pedido.id] = time.time()
            self.pila_deshacer.push(('preparar', pedido.id))
        return pedido

    def marcar_listo(self, id_pedido):
        self.dao.actualizar_estado(id_pedido, 'listo')
        pedido = self.dao.obtener_por_id(id_pedido)
        self._cargar_detalles(pedido)
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

    def devolver_a_cola(self, id_pedido):
        self.dao.actualizar_estado(id_pedido, 'en_cola')
        pedido = self.dao.obtener_por_id(id_pedido)
        if pedido:
            self._cargar_detalles(pedido)
            pedido.estado = 'en_cola'
            self.cola_pedidos.enqueue(pedido)
        self._inicio_preparacion.pop(id_pedido, None)
        self.lista_pendientes.eliminar(pedido)
        return pedido

    def devolver_a_espera(self, id_pedido):
        self.dao.actualizar_estado(id_pedido, 'espera')
        pedido = self.dao.obtener_por_id(id_pedido)
        if pedido:
            self._cargar_detalles(pedido)
            pedido.estado = 'espera'
            self.cola_espera.enqueue(pedido)
        self._inicio_preparacion.pop(id_pedido, None)
        self.lista_pendientes.eliminar(pedido)
        return pedido

    def devolver_a_cola(self, id_pedido):
        self.dao.actualizar_estado(id_pedido, 'en_cola')
        for p in self.cola_espera.recorrer():
            if p.id == id_pedido:
                p.estado = 'en_cola'
        pedido = self.dao.obtener_por_id(id_pedido)
        if pedido:
            self._cargar_detalles(pedido)
            pedido.estado = 'en_cola'
            self.cola_pedidos.enqueue(pedido)
        self._inicio_preparacion.pop(id_pedido, None)
        self.lista_pendientes.eliminar(pedido)
        return pedido

    def deshacer_ultima_accion(self):
        accion = self.pila_deshacer.pop()
        if not accion:
            return None
        tipo, id_pedido = accion
        if tipo == 'crear':
            self.dao.actualizar_estado(id_pedido, 'cancelado')
            for p in self.cola_pedidos.recorrer():
                if p.id == id_pedido:
                    p.estado = 'cancelado'
            return f'Pedido #{id_pedido} cancelado'
        elif tipo == 'espera':
            self.dao.actualizar_estado(id_pedido, 'en_cola')
            for p in self.cola_espera.recorrer():
                if p.id == id_pedido:
                    p.estado = 'en_cola'
            pedido = self.dao.obtener_por_id(id_pedido)
            if pedido:
                self._cargar_detalles(pedido)
                self.cola_pedidos.enqueue(pedido)
            return f'Pedido #{id_pedido} devuelto a cola'
        elif tipo == 'preparar':
            self.dao.actualizar_estado(id_pedido, 'espera')
            for p in self.lista_pendientes:
                if p.id == id_pedido:
                    p.estado = 'espera'
            self._inicio_preparacion.pop(id_pedido, None)
            pedido = self.dao.obtener_por_id(id_pedido)
            if pedido:
                self._cargar_detalles(pedido)
                self.cola_espera.enqueue(pedido)
            return f'Pedido #{id_pedido} devuelto a espera'
        elif tipo == 'listo':
            self.dao.actualizar_estado(id_pedido, 'preparacion')
            return f'Pedido #{id_pedido} devuelto a preparación'
        return None

    def obtener_cola(self):
        resultado = []
        for p in self.cola_pedidos.recorrer():
            if p.estado == 'en_cola':
                self._cargar_detalles(p)
                resultado.append(p)
        return resultado

    def obtener_espera(self):
        resultado = []
        for p in self.cola_espera.recorrer():
            if p.estado == 'espera':
                self._cargar_detalles(p)
                resultado.append(p)
        return resultado

    def obtener_pendientes(self):
        resultado = []
        for pedido in self.lista_pendientes:
            if pedido.estado == 'preparacion':
                self._cargar_detalles(pedido)
                resultado.append(pedido)
        return resultado

    def obtener_tiempo_preparacion(self, id_pedido):
        inicio = self._inicio_preparacion.get(id_pedido)
        if inicio:
            return int(time.time() - inicio)
        return 0

    def obtener_pila_deshacer(self):
        return self.pila_deshacer.recorrer()

    def obtener_pedidos_recientes(self, limite=5):
        return self.dao.listar()[:limite]

    def buscar_clientes(self, query=''):
        return self.cliente_dao.buscar(query) if query else self.cliente_dao.listar()

    def crear_cliente(self, nombre, telefono='', email=''):
        cliente = Cliente(nombre=nombre, telefono=telefono, email=email)
        cliente.id = self.cliente_dao.insertar(cliente)
        return cliente
