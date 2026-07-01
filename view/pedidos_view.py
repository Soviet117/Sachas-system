import customtkinter as ctk
from controller.pedido_controller import PedidoController
from controller.producto_controller import ProductoController
from controller.cliente_controller import ClienteController


class PedidosView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color='transparent')
        self.app = app
        self.ctrl = PedidoController()
        self.prod_ctrl = ProductoController()
        self.cli_ctrl = ClienteController()
        self._items_seleccionados = []

        label = ctk.CTkLabel(
            self, text='🧾 Gestión de Pedidos',
            font=ctk.CTkFont(size=28, weight='bold'), anchor='w'
        )
        label.pack(fill='x', padx=30, pady=(25, 5))

        sub = ctk.CTkLabel(
            self, text='Visualiza la cola FIFO de pedidos en tiempo real',
            font=ctk.CTkFont(size=14), text_color='#888888', anchor='w'
        )
        sub.pack(fill='x', padx=30, pady=(0, 15))

        container = ctk.CTkFrame(self, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=25, pady=5)
        container.grid_columnconfigure(0, weight=2)
        container.grid_columnconfigure(1, weight=3)
        container.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(container, fg_color='#16213e', corner_radius=12, border_width=1, border_color='#2a2a4a')
        left.grid(row=0, column=0, sticky='nsew', padx=5)

        ctk.CTkLabel(left, text='➕ Nuevo Pedido',
                     font=ctk.CTkFont(size=16, weight='bold')).pack(pady=(12, 10))

        self._cliente_menu = ctk.CTkOptionMenu(left, values=[], width=200)
        self._cliente_menu.pack(pady=5)
        self._cargar_clientes()

        self._prod_frame = ctk.CTkScrollableFrame(left, fg_color='transparent', height=250)
        self._prod_frame.pack(fill='both', expand=True, padx=10, pady=5)
        self._cargar_productos()

        ctk.CTkButton(left, text='➕ Agregar a Pedido', command=self._agregar_item).pack(pady=8)

        right = ctk.CTkFrame(container, fg_color='#16213e', corner_radius=12, border_width=1, border_color='#2a2a4a')
        right.grid(row=0, column=1, sticky='nsew', padx=5)

        self._build_panel_derecho(right)

    def _build_panel_derecho(self, parent):
        tab = ctk.CTkTabview(parent, fg_color='transparent')
        tab.pack(fill='both', expand=True, padx=5, pady=5)

        cola_tab = tab.add('⏳ Cola FIFO')
        prep_tab = tab.add('👨‍🍳 Preparación')
        items_tab = tab.add('🛒 Items')

        self._cola_frame = ctk.CTkScrollableFrame(cola_tab, fg_color='transparent')
        self._cola_frame.pack(fill='both', expand=True, padx=5, pady=5)

        btn_pasar = ctk.CTkButton(cola_tab, text='➡️ Pasar a Preparación', command=self._pasar_preparacion)
        btn_pasar.pack(pady=5)

        self._prep_frame = ctk.CTkScrollableFrame(prep_tab, fg_color='transparent')
        self._prep_frame.pack(fill='both', expand=True, padx=5, pady=5)

        btn_listo = ctk.CTkButton(prep_tab, text='✅ Marcar como Listo', command=self._marcar_listo)
        btn_listo.pack(pady=5)

        self._items_frame = ctk.CTkScrollableFrame(items_tab, fg_color='transparent')
        self._items_frame.pack(fill='both', expand=True, padx=5, pady=5)

        btn_crear = ctk.CTkButton(items_tab, text='📝 Crear Pedido', command=self._crear_pedido)
        btn_crear.pack(pady=5)

        ctk.CTkButton(parent, text='↩️ Deshacer (Ctrl+Z)', command=self._deshacer,
                      fg_color='#7B241C', hover_color='#922B21').pack(pady=5, padx=15, fill='x')

    def on_activate(self):
        self._refrescar()

    def _cargar_clientes(self):
        clientes = self.cli_ctrl.listar()
        self._clientes = clientes
        self._cliente_menu.configure(values=[c.nombre for c in clientes])
        if clientes:
            self._cliente_menu.set(clientes[0].nombre)

    def _cargar_productos(self):
        for w in self._prod_frame.winfo_children():
            w.destroy()
        productos = self.prod_ctrl.listar()
        self._var_cache = {}
        for p in productos:
            var = ctk.IntVar(value=0)
            self._var_cache[p.id] = var
            row = ctk.CTkFrame(self._prod_frame, fg_color='transparent')
            row.pack(fill='x', pady=1)
            ctk.CTkLabel(row, text=p.nombre, font=ctk.CTkFont(size=12), anchor='w').pack(side='left', fill='x', expand=True)
            ctk.CTkLabel(row, text=f'S/{p.precio:.2f}', font=ctk.CTkFont(size=11), text_color='#2ECC71', width=60).pack(side='right')
            spin = ctk.CTkEntry(row, width=40, textvariable=var)
            spin.pack(side='right', padx=3)
            ctk.CTkLabel(row, text='Cant:', font=ctk.CTkFont(size=11), width=35).pack(side='right')

    def _agregar_item(self):
        productos = self.prod_ctrl.listar()
        for p in productos:
            cantidad = self._var_cache.get(p.id, ctk.IntVar(value=0)).get()
            if cantidad > 0:
                existente = next((i for i in self._items_seleccionados if i['id_producto'] == p.id), None)
                if existente:
                    existente['cantidad'] += cantidad
                    existente['subtotal'] = existente['cantidad'] * p.precio
                else:
                    self._items_seleccionados.append({
                        'id_producto': p.id,
                        'nombre': p.nombre,
                        'cantidad': cantidad,
                        'precio': p.precio,
                        'subtotal': cantidad * p.precio
                    })
                self._var_cache[p.id].set(0)
        self._renderizar_items()

    def _renderizar_items(self):
        for w in self._items_frame.winfo_children():
            w.destroy()
        total = 0
        for i, item in enumerate(self._items_seleccionados):
            row = ctk.CTkFrame(self._items_frame, fg_color='transparent')
            row.pack(fill='x', pady=1)
            ctk.CTkLabel(row, text=item['nombre'], anchor='w', font=ctk.CTkFont(size=12)).pack(side='left', fill='x', expand=True)
            ctk.CTkLabel(row, text=f'x{item["cantidad"]}', width=40, font=ctk.CTkFont(size=11)).pack(side='right')
            ctk.CTkLabel(row, text=f'S/{item["subtotal"]:.2f}', width=70, font=ctk.CTkFont(size=11), text_color='#2ECC71').pack(side='right')
            total += item['subtotal']
        if self._items_seleccionados:
            sep = ctk.CTkFrame(self._items_frame, height=1, fg_color='#2ECC71')
            sep.pack(fill='x', pady=5)
            ctk.CTkLabel(self._items_frame, text=f'Total: S/{total:.2f}',
                         font=ctk.CTkFont(size=15, weight='bold'), text_color='#2ECC71').pack()

    def _crear_pedido(self):
        if not self._items_seleccionados:
            return
        nombre_cliente = self._cliente_menu.get()
        cliente = next((c for c in self._clientes if c.nombre == nombre_cliente), None)
        id_cliente = cliente.id if cliente else None

        self.ctrl.crear_pedido(id_cliente, self._items_seleccionados)
        self._items_seleccionados.clear()
        self._renderizar_items()
        self._refrescar()

    def _refrescar(self):
        self._renderizar_cola()
        self._renderizar_preparacion()

    def _renderizar_cola(self):
        for w in self._cola_frame.winfo_children():
            w.destroy()
        cola = self.ctrl.obtener_cola()
        if not cola:
            ctk.CTkLabel(self._cola_frame, text='⏳ Cola vacía', text_color='#666').pack(pady=20)
        for i, pedido in enumerate(cola):
            arrow = '📌' if i == 0 else '↓'
            row = ctk.CTkFrame(self._cola_frame, fg_color='#1a1a3e', corner_radius=8)
            row.pack(fill='x', pady=2)
            ctk.CTkLabel(row, text=f'{arrow} #{pedido.id}', width=50, font=ctk.CTkFont(size=12, weight='bold')).pack(side='left', padx=5)
            ctk.CTkLabel(row, text=pedido.cliente_nombre or 'General', font=ctk.CTkFont(size=12)).pack(side='left', fill='x', expand=True)
            ctk.CTkLabel(row, text=f'S/{pedido.total:.2f}', font=ctk.CTkFont(size=12), text_color='#2ECC71').pack(side='right', padx=10)

    def _renderizar_preparacion(self):
        for w in self._prep_frame.winfo_children():
            w.destroy()
        pendientes = self.ctrl.obtener_pendientes()
        if not pendientes:
            ctk.CTkLabel(self._prep_frame, text='👨‍🍳 Sin pedidos en preparación', text_color='#666').pack(pady=20)
        for pedido in pendientes:
            row = ctk.CTkFrame(self._prep_frame, fg_color='#1a1a3e', corner_radius=8)
            row.pack(fill='x', pady=2)
            ctk.CTkLabel(row, text=f'🍳 #{pedido.id}', width=50, font=ctk.CTkFont(size=12, weight='bold')).pack(side='left', padx=5)
            ctk.CTkLabel(row, text=pedido.cliente_nombre or 'General', font=ctk.CTkFont(size=12)).pack(side='left', fill='x', expand=True)
            ctk.CTkLabel(row, text=f'S/{pedido.total:.2f}', font=ctk.CTkFont(size=12), text_color='#F39C12').pack(side='right', padx=10)
            ctk.CTkButton(row, text='✅ Listo', width=70, height=28,
                          command=lambda pid=pedido.id: self._marcar_listo_id(pid)).pack(side='right', padx=5)

    def _pasar_preparacion(self):
        self.ctrl.pasar_a_preparacion()
        self._refrescar()

    def _marcar_listo(self):
        pendientes = self.ctrl.obtener_pendientes()
        if pendientes:
            self._marcar_listo_id(pendientes[0].id)

    def _marcar_listo_id(self, id_pedido):
        self.ctrl.marcar_listo(id_pedido)
        self._refrescar()

    def _deshacer(self):
        msg = self.ctrl.deshacer_ultima_accion()
        if msg:
            self._refrescar()