import customtkinter as ctk
from controller.venta_controller import VentaController
from controller.pedido_controller import PedidoController
from controller.producto_controller import ProductoController


class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color='transparent')
        self.app = app
        self.venta_ctrl = VentaController()
        self.pedido_ctrl = PedidoController()
        self.producto_ctrl = ProductoController()

        label = ctk.CTkLabel(
            self, text='📊 Dashboard',
            font=ctk.CTkFont(size=28, weight='bold'),
            anchor='w'
        )
        label.pack(fill='x', padx=30, pady=(25, 5))

        sub = ctk.CTkLabel(
            self, text='Resumen del día en Sachas Café',
            font=ctk.CTkFont(size=14),
            text_color='#888888', anchor='w'
        )
        sub.pack(fill='x', padx=30, pady=(0, 20))

        self._build_kpi_cards()
        self._build_tables()

    def on_activate(self):
        self._actualizar()

    def _crear_card_kpi(self, parent, titulo, valor, icono, color):
        card = ctk.CTkFrame(parent, fg_color='#16213e', corner_radius=12, border_width=1, border_color='#2a2a4a')
        card.pack(side='left', fill='both', expand=True, padx=8, pady=5)

        icon_label = ctk.CTkLabel(card, text=icono, font=ctk.CTkFont(size=32))
        icon_label.pack(pady=(15, 5))

        valor_label = ctk.CTkLabel(
            card, text=valor,
            font=ctk.CTkFont(size=28, weight='bold'),
            text_color=color
        )
        valor_label.pack()

        ctk.CTkLabel(
            card, text=titulo,
            font=ctk.CTkFont(size=13),
            text_color='#999999'
        ).pack(pady=(2, 15))

        return valor_label

    def _build_kpi_cards(self):
        cards_frame = ctk.CTkFrame(self, fg_color='transparent')
        cards_frame.pack(fill='x', padx=25, pady=5)

        ventas = self.venta_ctrl.ventas_del_dia()
        num_ventas = self.venta_ctrl.contar_ventas_del_dia()
        cola = len(self.pedido_ctrl.obtener_cola())
        productos = len(self.producto_ctrl.listar())

        self._crear_card_kpi(cards_frame, 'Ventas Hoy', f'S/{ventas:.2f}', '💰', '#2ECC71')
        self._crear_card_kpi(cards_frame, 'Pedidos Hoy', str(num_ventas), '🧾', '#3498DB')
        self._crear_card_kpi(cards_frame, 'En Cola', str(cola), '⏳', '#F39C12')
        self._crear_card_kpi(cards_frame, 'Productos', str(productos), '📦', '#9B59B6')

    def _build_tables(self):
        container = ctk.CTkFrame(self, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=25, pady=10)
        container.grid_columnconfigure(0, weight=1, uniform='a')
        container.grid_columnconfigure(1, weight=1, uniform='a')
        container.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(container, fg_color='#16213e', corner_radius=12, border_width=1, border_color='#2a2a4a')
        left.grid(row=0, column=0, sticky='nsew', padx=5)

        ctk.CTkLabel(
            left, text='🏆  Top Productos del Día',
            font=ctk.CTkFont(size=16, weight='bold')
        ).pack(anchor='w', padx=15, pady=(12, 8))

        self._top_frame = ctk.CTkScrollableFrame(left, fg_color='transparent', height=200)
        self._top_frame.pack(fill='both', expand=True, padx=10, pady=5)

        right = ctk.CTkFrame(container, fg_color='#16213e', corner_radius=12, border_width=1, border_color='#2a2a4a')
        right.grid(row=0, column=1, sticky='nsew', padx=5)

        ctk.CTkLabel(
            right, text='🕐  Pedidos Recientes',
            font=ctk.CTkFont(size=16, weight='bold')
        ).pack(anchor='w', padx=15, pady=(12, 8))

        self._recent_frame = ctk.CTkScrollableFrame(right, fg_color='transparent', height=200)
        self._recent_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self._actualizar_tablas()

    def _actualizar(self):
        ventas = self.venta_ctrl.ventas_del_dia()
        num_ventas = self.venta_ctrl.contar_ventas_del_dia()
        cola = len(self.pedido_ctrl.obtener_cola())
        productos = len(self.producto_ctrl.listar())

        widgets = self.winfo_children()
        for w in widgets:
            if isinstance(w, ctk.CTkFrame):
                for child in w.winfo_children():
                    if isinstance(child, ctk.CTkFrame):
                        labels = child.winfo_children()
                        if len(labels) >= 2 and isinstance(labels[1], ctk.CTkLabel):
                            texts = ['S/%.2f' % ventas, str(num_ventas), str(cola), str(productos)]
                            for i, l in enumerate([w2 for w2 in self.winfo_children() if isinstance(w2, ctk.CTkFrame)][0].winfo_children()):
                                inner_labels = l.winfo_children()
                                for il in inner_labels:
                                    if isinstance(il, ctk.CTkLabel) and il.cget('font').cget('size') == 28:
                                        if i < len(texts):
                                            il.configure(text=texts[i])
        self._actualizar_tablas()

    def _actualizar_tablas(self):
        for w in self._top_frame.winfo_children():
            w.destroy()
        for w in self._recent_frame.winfo_children():
            w.destroy()

        top = self.venta_ctrl.top_productos(5)
        if top:
            for i, (nombre, cantidad) in enumerate(top, 1):
                bg = '#1a1a3e' if i % 2 == 0 else 'transparent'
                row = ctk.CTkFrame(self._top_frame, fg_color=bg, corner_radius=6)
                row.pack(fill='x', pady=2)
                ctk.CTkLabel(row, text=f'{i}.', width=30, font=ctk.CTkFont(size=13)).pack(side='left', padx=5)
                ctk.CTkLabel(row, text=nombre, font=ctk.CTkFont(size=13)).pack(side='left', fill='x', expand=True)
                ctk.CTkLabel(row, text=f'x{cantidad}', font=ctk.CTkFont(size=13), text_color='#2ECC71').pack(side='right', padx=10)
        else:
            ctk.CTkLabel(self._top_frame, text='Aún no hay ventas hoy', text_color='#666').pack(pady=20)

        recientes = self.pedido_ctrl.obtener_pedidos_recientes(8)
        if recientes:
            for pedido in recientes:
                estados = {'en_cola': '⏳ En cola', 'preparacion': '👨‍🍳 Preparando', 'listo': '✅ Listo', 'completado': '✔ Completado', 'cancelado': '❌ Cancelado'}
                estado = estados.get(pedido.estado, pedido.estado)
                row = ctk.CTkFrame(self._recent_frame, fg_color='#1a1a3e', corner_radius=6)
                row.pack(fill='x', pady=2)
                ctk.CTkLabel(row, text=f'#{pedido.id}', width=40, font=ctk.CTkFont(size=12, weight='bold')).pack(side='left', padx=5)
                ctk.CTkLabel(row, text=f'S/{pedido.total:.2f}', font=ctk.CTkFont(size=12)).pack(side='right', padx=5)
                ctk.CTkLabel(row, text=estado, font=ctk.CTkFont(size=12), text_color='#888').pack(side='right', padx=5)
        else:
            ctk.CTkLabel(self._recent_frame, text='No hay pedidos aún', text_color='#666').pack(pady=20)