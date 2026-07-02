import time
import customtkinter as ctk
from controller.pedido_controller import PedidoController
from controller.producto_controller import ProductoController
from model.entities.cliente import Cliente


class PedidosView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color='transparent')
        self.app = app
        self.ctrl = PedidoController()
        self.prod_ctrl = ProductoController()
        self._items_seleccionados = []
        self._cliente_seleccionado = None
        self._timer_id = None
        self._timer_ejecutando = False
        self._qty_vars = {}

        label = ctk.CTkLabel(
            self, text='🧾 Gestión de Pedidos',
            font=ctk.CTkFont(size=28, weight='bold'), anchor='w'
        )
        label.pack(fill='x', padx=30, pady=(25, 5))

        sub = ctk.CTkLabel(
            self, text='Cola FIFO → Pedidos en espera → Preparación',
            font=ctk.CTkFont(size=14), text_color='#888888', anchor='w'
        )
        sub.pack(fill='x', padx=30, pady=(0, 15))

        container = ctk.CTkFrame(self, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=25, pady=5)
        container.grid_columnconfigure(0, weight=2)
        container.grid_columnconfigure(1, weight=3)
        container.grid_rowconfigure(0, weight=1)

        self._build_panel_izquierdo(container)
        self._build_panel_derecho(container)

    def _build_panel_izquierdo(self, container):
        left = ctk.CTkFrame(container, fg_color='#16213e', corner_radius=12, border_width=1, border_color='#2a2a4a')
        left.grid(row=0, column=0, sticky='nsew', padx=5)

        ctk.CTkLabel(left, text='➕ Nuevo Pedido',
                     font=ctk.CTkFont(size=16, weight='bold')).pack(pady=(12, 10))

        cliente_frame = ctk.CTkFrame(left, fg_color='#0d1b2a', corner_radius=8)
        cliente_frame.pack(fill='x', padx=15, pady=5)

        self._cliente_label = ctk.CTkLabel(
            cliente_frame, text='👤 Cliente: Ninguno seleccionado',
            font=ctk.CTkFont(size=13), text_color='#888888'
        )
        self._cliente_label.pack(pady=(8, 2), padx=10)

        ctk.CTkButton(
            cliente_frame, text='🔍 Buscar / Crear Cliente',
            command=self._abrir_ventana_cliente,
            fg_color='#1a3d2e', hover_color='#2ECC71', height=32
        ).pack(pady=(2, 8), padx=10, fill='x')

        prod_label_frame = ctk.CTkFrame(left, fg_color='transparent')
        prod_label_frame.pack(fill='x', padx=15, pady=(10, 2))
        ctk.CTkLabel(prod_label_frame, text='Productos:',
                     font=ctk.CTkFont(size=13, weight='bold')).pack(side='left')
        ctk.CTkLabel(prod_label_frame, text='(ajusta cantidad y se agrega solo)',
                     font=ctk.CTkFont(size=10), text_color='#888').pack(side='left', padx=8)

        self._prod_frame = ctk.CTkScrollableFrame(left, fg_color='transparent', height=180)
        self._prod_frame.pack(fill='both', expand=True, padx=10, pady=2)

        resumen_frame = ctk.CTkFrame(left, fg_color='#0d1b2a', corner_radius=8)
        resumen_frame.pack(fill='x', padx=15, pady=(5, 2))

        ctk.CTkLabel(resumen_frame, text='📋 Resumen del Pedido',
                     font=ctk.CTkFont(size=12, weight='bold')).pack(pady=(6, 2))

        self._resumen_text = ctk.CTkLabel(
            resumen_frame, text='Sin productos agregados',
            font=ctk.CTkFont(size=11), text_color='#888', anchor='w', justify='left'
        )
        self._resumen_text.pack(fill='x', padx=10, pady=(0, 6))

        ctk.CTkButton(left, text='📝 Crear Pedido', height=38,
                      fg_color='#1E8449', hover_color='#2ECC71',
                      command=self._crear_pedido).pack(pady=(8, 12), padx=15, fill='x')

        self._cargar_productos()

    def _build_panel_derecho(self, container):
        right = ctk.CTkFrame(container, fg_color='#16213e', corner_radius=12, border_width=1, border_color='#2a2a4a')
        right.grid(row=0, column=1, sticky='nsew', padx=5)

        tab = ctk.CTkTabview(right, fg_color='transparent')
        tab.pack(fill='both', expand=True, padx=5, pady=5)

        cola_tab = tab.add('⏳ Cola FIFO')
        espera_tab = tab.add('🕐 Pedidos en espera')
        prep_tab = tab.add('👨‍🍳 Preparación')

        ctk.CTkLabel(cola_tab, text='Pedidos recién creados esperando su turno',
                     font=ctk.CTkFont(size=11), text_color='#888').pack(pady=(5, 0))

        self._cola_frame = ctk.CTkScrollableFrame(cola_tab, fg_color='transparent')
        self._cola_frame.pack(fill='both', expand=True, padx=5, pady=5)

        ctk.CTkButton(cola_tab, text='➡️ Mover a Espera',
                      command=self._mover_a_espera).pack(pady=5)

        ctk.CTkLabel(espera_tab, text='Pedidos en cola de espera para preparación',
                     font=ctk.CTkFont(size=11), text_color='#888').pack(pady=(5, 0))

        self._espera_frame = ctk.CTkScrollableFrame(espera_tab, fg_color='transparent')
        self._espera_frame.pack(fill='both', expand=True, padx=5, pady=5)

        ctk.CTkButton(espera_tab, text='➡️ Pasar a Preparación',
                      command=self._pasar_preparacion).pack(pady=5)

        ctk.CTkLabel(prep_tab, text='Pedidos en preparación con temporizador',
                     font=ctk.CTkFont(size=11), text_color='#888').pack(pady=(5, 0))

        self._prep_frame = ctk.CTkScrollableFrame(prep_tab, fg_color='transparent')
        self._prep_frame.pack(fill='both', expand=True, padx=5, pady=5)

        ctk.CTkButton(prep_tab, text='✅ Marcar como Listo',
                      command=self._marcar_listo).pack(pady=5)

        ctk.CTkButton(right, text='↩️ Deshacer (Ctrl+Z)', command=self._deshacer,
                      fg_color='#7B241C', hover_color='#922B21').pack(pady=5, padx=15, fill='x')

    def on_activate(self):
        self._refrescar()
        self._iniciar_timers()

    def _iniciar_timers(self):
        if self._timer_ejecutando:
            return
        self._timer_ejecutando = True
        self._programar_actualizacion_timers()

    def _cargar_productos(self):
        for w in self._prod_frame.winfo_children():
            w.destroy()
        self._qty_vars = {}
        productos = self.prod_ctrl.listar()
        for p in productos:
            var = ctk.StringVar(value='0')
            var.trace_add('write', lambda *args, pid=p.id: self._on_qty_change(pid))
            self._qty_vars[p.id] = var
            row = ctk.CTkFrame(self._prod_frame, fg_color='transparent')
            row.pack(fill='x', pady=1)
            ctk.CTkLabel(row, text=p.nombre, font=ctk.CTkFont(size=12), anchor='w').pack(side='left', fill='x', expand=True)
            ctk.CTkLabel(row, text=f'S/{p.precio:.2f}', font=ctk.CTkFont(size=11), text_color='#2ECC71', width=60).pack(side='right')
            spin = ctk.CTkEntry(row, width=40, textvariable=var)
            spin.pack(side='right', padx=3)
            ctk.CTkLabel(row, text='Cant:', font=ctk.CTkFont(size=11), width=35).pack(side='right')

    def _on_qty_change(self, id_producto):
        if hasattr(self, '_qty_debounce') and self._qty_debounce:
            self.after_cancel(self._qty_debounce)
        self._qty_debounce = self.after(100, self._actualizar_resumen)

    def _actualizar_resumen(self):
        self._items_seleccionados.clear()
        productos = self.prod_ctrl.listar()
        for p in productos:
            var = self._qty_vars.get(p.id)
            if not var:
                continue
            try:
                cantidad = int(var.get())
            except (ValueError, TypeError):
                cantidad = 0
            if cantidad > 0:
                self._items_seleccionados.append({
                    'id_producto': p.id,
                    'nombre': p.nombre,
                    'cantidad': cantidad,
                    'precio': p.precio,
                    'subtotal': cantidad * p.precio
                })
        if not self._items_seleccionados:
            self._resumen_text.configure(text='Sin productos agregados', text_color='#888')
            return
        total = 0
        lineas = []
        for item in self._items_seleccionados:
            lineas.append(f'{item["nombre"]} x{item["cantidad"]} = S/{item["subtotal"]:.2f}')
            total += item['subtotal']
        lineas.append(f'')
        lineas.append(f'Total: S/{total:.2f}')
        self._resumen_text.configure(text='\n'.join(lineas), text_color='#2ECC71')

    def _abrir_ventana_cliente(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title('Seleccionar / Crear Cliente')
        dialog.geometry('520x550')
        dialog.transient(self)
        dialog.grab_set()
        dialog.focus()

        ctk.CTkLabel(dialog, text='👤 Seleccionar Cliente',
                     font=ctk.CTkFont(size=18, weight='bold')).pack(pady=(15, 5))
        ctk.CTkLabel(dialog, text='Busca un cliente existente o crea uno nuevo',
                     font=ctk.CTkFont(size=12), text_color='#888888').pack(pady=(0, 10))

        search_entry = ctk.CTkEntry(dialog, placeholder_text='Buscar por nombre o teléfono...')
        search_entry.pack(fill='x', padx=25, pady=5)

        results_frame = ctk.CTkScrollableFrame(dialog, fg_color='transparent', height=280)
        results_frame.pack(fill='both', expand=True, padx=25, pady=5)

        status_label = ctk.CTkLabel(dialog, text='', font=ctk.CTkFont(size=12), text_color='#2ECC71')
        status_label.pack()

        nuevo_btn = ctk.CTkButton(dialog, text='+ Nuevo Cliente', command=lambda: None)
        nuevo_btn.pack(pady=5)
        ctk.CTkButton(dialog, text='Cancelar', fg_color='#7B241C', hover_color='#922B21',
                      command=dialog.destroy).pack(pady=(0, 10))

        def seleccionar(cliente):
            self._cliente_seleccionado = cliente
            self._cliente_label.configure(
                text=f'👤 Cliente: {cliente.nombre}',
                text_color='#2ECC71'
            )
            dialog.destroy()

        def bind_click(w, cl):
            w.bind('<Button-1>', lambda e, cl=cl: seleccionar(cl))
            for child in w.winfo_children():
                bind_click(child, cl)

        def mostrar_resultados(query=''):
            for w in results_frame.winfo_children():
                w.destroy()
            status_label.configure(text='')
            try:
                clientes = self.ctrl.buscar_clientes(query) if query else self.ctrl.buscar_clientes()
            except Exception:
                clientes = []
            if not clientes:
                ctk.CTkLabel(results_frame, text='Sin resultados. Crea un nuevo cliente.',
                             text_color='#666').pack(pady=20)
                return
            for c in clientes:
                card = ctk.CTkFrame(results_frame, fg_color='#1a1a3e', corner_radius=8,
                                    border_width=1, border_color='#2a2a4a')
                card.pack(fill='x', pady=2, padx=2)
                info = ctk.CTkFrame(card, fg_color='transparent')
                info.pack(fill='x', padx=10, pady=6)
                ctk.CTkLabel(info, text=c.nombre, font=ctk.CTkFont(size=14, weight='bold'),
                             anchor='w').pack(fill='x')
                ctk.CTkLabel(info, text=f'📞 {c.telefono or "—"}  ✉️ {c.email or "—"}  ⭐ {c.puntos} pts',
                             font=ctk.CTkFont(size=11), text_color='#AAAAAA', anchor='w').pack(fill='x')
                bind_click(card, c)

        def mostrar_formulario_nuevo():
            for w in results_frame.winfo_children():
                w.destroy()
            nuevo_btn.pack_forget()
            status_label.configure(text='')

            form_frame = ctk.CTkFrame(results_frame, fg_color='transparent')
            form_frame.pack(fill='both', expand=True, pady=10)

            ctk.CTkLabel(form_frame, text='📝 Nuevo Cliente',
                         font=ctk.CTkFont(size=15, weight='bold')).pack(pady=(0, 10))

            entries = {}
            for key, label, req in [('nombre', 'Nombre *', True), ('telefono', 'Teléfono', False), ('email', 'Email', False)]:
                ctk.CTkLabel(form_frame, text=label, font=ctk.CTkFont(size=13)).pack(anchor='w', padx=10, pady=(8, 2))
                entry = ctk.CTkEntry(form_frame, placeholder_text=label)
                entry.pack(fill='x', padx=10)
                entries[key] = entry

            error_lbl = ctk.CTkLabel(form_frame, text='', text_color='#E74C3C', font=ctk.CTkFont(size=12))
            error_lbl.pack()

            def guardar_nuevo():
                nombre = entries['nombre'].get().strip()
                if not nombre:
                    error_lbl.configure(text='El nombre es obligatorio')
                    return
                try:
                    c = self.ctrl.crear_cliente(
                        nombre=nombre,
                        telefono=entries['telefono'].get().strip(),
                        email=entries['email'].get().strip()
                    )
                    seleccionar(c)
                except Exception as e:
                    error_lbl.configure(text=f'Error: {e}')

            btn_frame = ctk.CTkFrame(form_frame, fg_color='transparent')
            btn_frame.pack(fill='x', pady=15)
            ctk.CTkButton(btn_frame, text='Guardar', command=guardar_nuevo,
                          fg_color='#1E8449', hover_color='#2ECC71').pack(side='left', padx=5, expand=True)
            ctk.CTkButton(btn_frame, text='← Volver', command=lambda: volver_resultados(),
                          fg_color='#555', hover_color='#777').pack(side='left', padx=5, expand=True)

        def volver_resultados():
            nuevo_btn.pack(pady=5)
            mostrar_resultados(search_entry.get())

        search_entry.bind('<KeyRelease>', lambda e: mostrar_resultados(search_entry.get()))
        nuevo_btn.configure(command=mostrar_formulario_nuevo)
        mostrar_resultados()
        search_entry.focus()

    def _crear_pedido(self):
        if not self._items_seleccionados:
            return
        id_cliente = self._cliente_seleccionado.id if self._cliente_seleccionado else None
        self.ctrl.crear_pedido(id_cliente, self._items_seleccionados)
        for var in self._qty_vars.values():
            var.set('0')
        self._items_seleccionados.clear()
        self._actualizar_resumen()
        self._refrescar()

    def _refrescar(self):
        self._renderizar_cola()
        self._renderizar_espera()
        self._renderizar_preparacion()

    def _renderizar_cola(self):
        for w in self._cola_frame.winfo_children():
            w.destroy()
        cola = self.ctrl.obtener_cola()
        if not cola:
            ctk.CTkLabel(self._cola_frame, text='⏳ Cola vacía',
                         text_color='#666', font=ctk.CTkFont(size=13)).pack(pady=30)
            return
        for i, pedido in enumerate(cola):
            es_primero = (i == 0)
            border = '#3498DB' if es_primero else '#2a2a4a'
            bg = '#1a2a4e' if es_primero else '#1a1a3e'

            card = ctk.CTkFrame(self._cola_frame, fg_color=bg, corner_radius=10,
                                border_width=2 if es_primero else 1, border_color=border)
            card.pack(fill='x', pady=4, padx=2)

            hdr = ctk.CTkFrame(card, fg_color='transparent')
            hdr.pack(fill='x', padx=12, pady=(8, 2))
            icono = '📌 ' if es_primero else '↓ '
            ctk.CTkLabel(hdr, text=f'{icono}#{pedido.id}',
                         font=ctk.CTkFont(size=14, weight='bold'), text_color='#3498DB').pack(side='left')
            ctk.CTkLabel(hdr, text=pedido.cliente_nombre or 'General',
                         font=ctk.CTkFont(size=13), anchor='w').pack(side='left', fill='x', expand=True, padx=8)
            ctk.CTkLabel(hdr, text=f'S/{pedido.total:.2f}',
                         font=ctk.CTkFont(size=14, weight='bold'), text_color='#2ECC71').pack(side='right')

            if pedido.detalles:
                body = ctk.CTkFrame(card, fg_color='transparent')
                body.pack(fill='x', padx=12, pady=(2, 6))
                for d in pedido.detalles[:4]:
                    ctk.CTkLabel(body, text=f'  • {d.producto_nombre} x{d.cantidad}',
                                 font=ctk.CTkFont(size=11), text_color='#AAAAAA', anchor='w').pack(fill='x')
                if len(pedido.detalles) > 4:
                    ctk.CTkLabel(body, text=f'  ... +{len(pedido.detalles) - 4} más',
                                 font=ctk.CTkFont(size=10), text_color='#666').pack(anchor='w')

            if es_primero:
                bf = ctk.CTkFrame(card, fg_color='transparent')
                bf.pack(fill='x', padx=12, pady=(0, 8))
                ctk.CTkButton(bf, text='➡️ Mover a Espera', height=30,
                              font=ctk.CTkFont(size=12),
                              command=self._mover_a_espera).pack(side='right')

    def _renderizar_espera(self):
        for w in self._espera_frame.winfo_children():
            w.destroy()
        espera = self.ctrl.obtener_espera()
        if not espera:
            ctk.CTkLabel(self._espera_frame, text='🕐 Sin pedidos en espera',
                         text_color='#666', font=ctk.CTkFont(size=13)).pack(pady=30)
            return
        for i, pedido in enumerate(espera):
            es_primero = (i == 0)
            border = '#F39C12' if es_primero else '#2a2a4a'
            bg = '#2a2a1a' if es_primero else '#1a1a3e'

            card = ctk.CTkFrame(self._espera_frame, fg_color=bg, corner_radius=10,
                                border_width=2 if es_primero else 1, border_color=border)
            card.pack(fill='x', pady=4, padx=2)

            hdr = ctk.CTkFrame(card, fg_color='transparent')
            hdr.pack(fill='x', padx=12, pady=(8, 2))
            icono = '🕐 ' if es_primero else '↓ '
            ctk.CTkLabel(hdr, text=f'{icono}#{pedido.id}',
                         font=ctk.CTkFont(size=14, weight='bold'), text_color='#F39C12').pack(side='left')
            ctk.CTkLabel(hdr, text=pedido.cliente_nombre or 'General',
                         font=ctk.CTkFont(size=13), anchor='w').pack(side='left', fill='x', expand=True, padx=8)
            ctk.CTkLabel(hdr, text=f'S/{pedido.total:.2f}',
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

            if es_primero:
                bf = ctk.CTkFrame(card, fg_color='transparent')
                bf.pack(fill='x', padx=12, pady=(0, 8))
                ctk.CTkButton(bf, text='➡️ Pasar a Preparación', height=30,
                              font=ctk.CTkFont(size=12),
                              command=self._pasar_preparacion).pack(side='right')

    def _renderizar_preparacion(self):
        for w in self._prep_frame.winfo_children():
            w.destroy()
        pendientes = self.ctrl.obtener_pendientes()
        if not pendientes:
            ctk.CTkLabel(self._prep_frame, text='👨‍🍳 Sin pedidos en preparación',
                         text_color='#666', font=ctk.CTkFont(size=13)).pack(pady=30)
            return
        for pedido in pendientes:
            tiempo = self.ctrl.obtener_tiempo_preparacion(pedido.id)
            mins, secs = divmod(tiempo, 60)

            card = ctk.CTkFrame(self._prep_frame, fg_color='#1a2e1a', corner_radius=10,
                                border_width=2, border_color='#F39C12')
            card.pack(fill='x', pady=4, padx=2)

            hdr = ctk.CTkFrame(card, fg_color='transparent')
            hdr.pack(fill='x', padx=12, pady=(8, 2))

            ctk.CTkLabel(hdr, text=f'🍳 #{pedido.id}',
                         font=ctk.CTkFont(size=14, weight='bold'), text_color='#F39C12').pack(side='left')
            ctk.CTkLabel(hdr, text=pedido.cliente_nombre or 'General',
                         font=ctk.CTkFont(size=13), anchor='w').pack(side='left', fill='x', expand=True, padx=8)
            timer_label = ctk.CTkLabel(hdr, text=f'⏱ {mins:02d}:{secs:02d}',
                                       font=ctk.CTkFont(size=14, weight='bold'), text_color='#FF6B6B')
            timer_label.pack(side='right')
            ctk.CTkLabel(hdr, text=f'S/{pedido.total:.2f}',
                         font=ctk.CTkFont(size=13), text_color='#2ECC71').pack(side='right', padx=8)

            if pedido.detalles:
                body = ctk.CTkFrame(card, fg_color='transparent')
                body.pack(fill='x', padx=12, pady=(2, 6))
                for d in pedido.detalles[:5]:
                    ctk.CTkLabel(body, text=f'  • {d.producto_nombre} x{d.cantidad} — S/{d.subtotal:.2f}',
                                 font=ctk.CTkFont(size=11), text_color='#CCCCCC', anchor='w').pack(fill='x')
                if len(pedido.detalles) > 5:
                    ctk.CTkLabel(body, text=f'  ... +{len(pedido.detalles) - 5} más',
                                 font=ctk.CTkFont(size=10), text_color='#666').pack(anchor='w')

            bf = ctk.CTkFrame(card, fg_color='transparent')
            bf.pack(fill='x', padx=12, pady=(4, 8))
            ctk.CTkButton(bf, text='✅ Listo', height=30, width=90,
                          font=ctk.CTkFont(size=12),
                          fg_color='#1E8449', hover_color='#2ECC71',
                          command=lambda pid=pedido.id: self._marcar_listo_id(pid)).pack(side='right', padx=2)
            ctk.CTkButton(bf, text='↩️ Devolver a Espera', height=30, width=120,
                          font=ctk.CTkFont(size=12),
                          fg_color='#7B241C', hover_color='#922B21',
                          command=lambda pid=pedido.id: self._devolver_espera(pid)).pack(side='right', padx=2)

            card._pedido_id = pedido.id
            card._timer_label = timer_label

        self._programar_actualizacion_timers()

    def _programar_actualizacion_timers(self):
        if self._timer_id:
            self.after_cancel(self._timer_id)
        self._actualizar_timers_prep()

    def _actualizar_timers_prep(self):
        if not self.winfo_exists():
            return
        for child in self._prep_frame.winfo_children():
            if hasattr(child, '_pedido_id') and hasattr(child, '_timer_label'):
                pid = child._pedido_id
                tiempo = self.ctrl.obtener_tiempo_preparacion(pid)
                mins, secs = divmod(tiempo, 60)
                child._timer_label.configure(text=f'⏱ {mins:02d}:{secs:02d}')
        self._timer_id = self.after(1000, self._actualizar_timers_prep)

    def _mover_a_espera(self):
        self.ctrl.pasar_a_espera()
        self._refrescar()

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

    def _devolver_espera(self, id_pedido):
        self.ctrl.devolver_a_espera(id_pedido)
        self._refrescar()

    def _deshacer(self):
        msg = self.ctrl.deshacer_ultima_accion()
        if msg:
            self._refrescar()
