from model.dao.venta_dao import VentaDAO


class VentaController:
    def __init__(self):
        self.dao = VentaDAO()

    def ventas_del_dia(self):
        return self.dao.ventas_del_dia()

    def contar_ventas_del_dia(self):
        return self.dao.contar_ventas_del_dia()

    def top_productos(self, limite=5):
        return self.dao.top_productos(limite)

    def listar(self):
        return self.dao.listar()