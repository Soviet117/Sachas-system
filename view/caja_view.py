import customtkinter as ctk
from controller.pedido_controller import PedidoController
from controller.venta_controller import VentaController


class CajaView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color='transparent')
        self.app = app
        self.pedido_ctrl = PedidoController()
        self.venta_ctrl = VentaController()

        label = ctk.CTkLabel(
            self, text='💰 Caja / Punto de Venta',
            font=ctk.CTkFont(size=28, weight='bold'), anchor='w'
        )
        label.pack(fill='x', padx=30, pady=(25, 5))

        sub = ctk.CTkLabel(
            self, text='Cobra pedidos listos y revisa las ventas del día',
            font=ctk.CTkFont(size=14), text_color='#888888', anchor='w'
        )
        sub.pack(fill='x', padx=30, pady=(0, 15))

        container = ctk.CTkFrame(self, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=25, pady=5)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(container, fg_color='#16213e', corner_radius=12, border_width=1, border_color='#2a2a4a')
        left.grid(row=0, column=0, sticky='nsew', padx=5)

        ctk.CTkLabel(left, text='✅ Pedidos Listos para Cobrar',
                     font=ctk.CTkFont(size=16, weight='bold')).pack(pady=(12, 10))

        self._listos_frame = ctk.CTkScrollableFrame(left, fg_color='transparent', height=300)
        self._listos_frame.pack(fill='both', expand=True, padx=10, pady=5)

        ctk.CTkLabel(left, text='Método de pago:',
                     font=ctk.CTkFont(size=13)).pack(anchor='w', padx=15)

        self._metodo_pago = ctk.CTkOptionMenu(left, values=['Efectivo', 'Tarjeta', 'Yape', 'Plin'])
        self._metodo_pago.pack(pady=5, padx=15, fill='x')

        self._info_label = ctk.CTkLabel(left, text='', font=ctk.CTkFont(size=14))
        self._info_label.pack(pady=5)

        right = ctk.CTkFrame(container, fg_color='#16213e', corner_radius=12, border_width=1, border_color='#2a2a4a')
        right.grid(row=0, column=1, sticky='nsew', padx=5)

        ctk.CTkLabel(right, text='📊 Resumen de Caja',
                     font=ctk.CTkFont(size=16, weight='bold')).pack(pady=(12, 10))

        self._resumen_frame = ctk.CTkFrame(right, fg_color='#0d1b2a', corner_radius=8)
        self._resumen_frame.pack(fill='x', padx=15, pady=10)

        self._total_dia_label = ctk.CTkLabel(
            self._resumen_frame, text='Total del día: S/ 0.00',
            font=ctk.CTkFont(size=20, weight='bold'), text_color='#2ECC71'
        )
        self._total_dia_label.pack(pady=(15, 5))

        self._num_ventas_label = ctk.CTkLabel(
            self._resumen_frame, text='Ventas realizadas: 0',
            font=ctk.CTkFont(size=14), text_color='#BBBBBB'
        )
        self._num_ventas_label.pack(pady=(0, 15))

        self._historial_frame = ctk.CTkScrollableFrame(right, fg_color='transparent', height=250)
        self._historial_frame.pack(fill='both', expand=True, padx=10, pady=5)

        ctk.CTkLabel(right, text='🕐 Últimas ventas:',
                     font=ctk.CTkFont(size=13, weight='bold')).pack(anchor='w', padx=15, pady=(5, 0))

        ctk.CTkButton(left, text='💵 Cobrar Pedido', height=40, fg_color='#1E8449',
                      hover_color='#2ECC71', command=self._cobrar).pack(pady=15, padx=15, fill='x')

    def on_activate(self):
        self._refrescar()

    def _refrescar(self):
        self._renderizar_listos()
        self._actualizar_resumen()
        self._renderizar_historial()

    def _renderizar_listos(self):
        for w in self._listos_frame.winfo_children():
            w.destroy()
        todos = self.pedido_ctrl.dao.listar()
        listos = [p for p in todos if p.estado == 'listo']
        if not listos:
            ctk.CTkLabel(self._listos_frame, text='No hay pedidos listos para cobrar',
                         text_color='#666', font=ctk.CTkFont(size=13)).pack(pady=30)
            return
        for pedido in listos:
            self.pedido_ctrl._cargar_detalles(pedido)

            card = ctk.CTkFrame(self._listos_frame, fg_color='#1a3e1a', corner_radius=10,
                                border_width=2, border_color='#2ECC71')
            card.pack(fill='x', pady=4, padx=2)

            header = ctk.CTkFrame(card, fg_color='transparent')
            header.pack(fill='x', padx=12, pady=(8, 2))

            ctk.CTkLabel(header, text=f'✅ #{pedido.id}',
                         font=ctk.CTkFont(size=14, weight='bold'), text_color='#2ECC71').pack(side='left')
            ctk.CTkLabel(header, text=pedido.cliente_nombre or 'General',
                         font=ctk.CTkFont(size=13), anchor='w').pack(side='left', fill='x', expand=True, padx=8)
            ctk.CTkLabel(header, text=f'S/{pedido.total:.2f}',
                         font=ctk.CTkFont(size=14, weight='bold'), text_color='#2ECC71').pack(side='right')

            if pedido.detalles:
                body = ctk.CTkFrame(card, fg_color='transparent')
                body.pack(fill='x', padx=12, pady=(2, 6))
                for d in pedido.detalles[:4]:
                    ctk.CTkLabel(body, text=f'  • {d.producto_nombre} x{d.cantidad}',
                                 font=ctk.CTkFont(size=11), text_color='#CCCCCC', anchor='w').pack(fill='x')
                if len(pedido.detalles) > 4:
                    ctk.CTkLabel(body, text=f'  ... +{len(pedido.detalles) - 4} más',
                                 font=ctk.CTkFont(size=10), text_color='#666').pack(anchor='w')

            btn_frame = ctk.CTkFrame(card, fg_color='transparent')
            btn_frame.pack(fill='x', padx=12, pady=(4, 8))
            ctk.CTkButton(btn_frame, text='💵 Cobrar', height=30,
                          font=ctk.CTkFont(size=12),
                          fg_color='#1E8449', hover_color='#2ECC71',
                          command=lambda pid=pedido.id: self._cobrar_id(pid)).pack(side='right', padx=2)

    def _actualizar_resumen(self):
        total = self.venta_ctrl.ventas_del_dia()
        num = self.venta_ctrl.contar_ventas_del_dia()
        self._total_dia_label.configure(text=f'Total del día: S/{total:.2f}')
        self._num_ventas_label.configure(text=f'Ventas realizadas: {num}')

    def _renderizar_historial(self):
        for w in self._historial_frame.winfo_children():
            w.destroy()
        ventas = self.venta_ctrl.listar()[:10]
        if not ventas:
            ctk.CTkLabel(self._historial_frame, text='Sin ventas aún',
                         text_color='#666').pack(pady=20)
            return
        for v in ventas:
            row = ctk.CTkFrame(self._historial_frame, fg_color='transparent')
            row.pack(fill='x', pady=1)
            ctk.CTkLabel(row, text=f'#{v.id_pedido}', width=40,
                         font=ctk.CTkFont(size=11)).pack(side='left', padx=5)
            ctk.CTkLabel(row, text=v.metodo_pago, width=60,
                         font=ctk.CTkFont(size=11)).pack(side='left')
            ctk.CTkLabel(row, text=f'S/{v.total:.2f}',
                         font=ctk.CTkFont(size=11),
                         text_color='#2ECC71').pack(side='right', padx=10)

    def _cobrar(self):
        todos = self.pedido_ctrl.dao.listar()
        listos = [p for p in todos if p.estado == 'listo']
        if listos:
            self._cobrar_id(listos[0].id)

    def _cobrar_id(self, id_pedido):
        metodo = self._metodo_pago.get().lower()
        self.pedido_ctrl.cobrar_pedido(id_pedido, metodo)
        pedido = self.pedido_ctrl.dao.obtener_por_id(id_pedido)
        self._info_label.configure(text=f'✅ Pedido #{id_pedido} cobrado — S/{pedido.total:.2f}',
                                   text_color='#2ECC71')
        self._refrescar()
