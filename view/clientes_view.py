import customtkinter as ctk
from controller.cliente_controller import ClienteController
from model.entities.cliente import Cliente


class ClientesView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color='transparent')
        self.app = app
        self.ctrl = ClienteController()
        self._clientes = []

        label = ctk.CTkLabel(
            self, text='Clientes',
            font=ctk.CTkFont(size=28, weight='bold'), anchor='w'
        )
        label.pack(fill='x', padx=30, pady=(25, 5))

        sub = ctk.CTkLabel(
            self, text='Registro de clientes y grafo de recomendaciones',
            font=ctk.CTkFont(size=14), text_color='#888888', anchor='w'
        )
        sub.pack(fill='x', padx=30, pady=(0, 15))

        toolbar = ctk.CTkFrame(self, fg_color='transparent')
        toolbar.pack(fill='x', padx=25, pady=5)

        self.search_entry = ctk.CTkEntry(toolbar, placeholder_text='Buscar cliente...', width=250)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self._buscar())

        ctk.CTkButton(toolbar, text='+ Nuevo Cliente', width=120, command=self._abrir_formulario).pack(side='left', padx=5)
        ctk.CTkButton(toolbar, text='🔗 Ver Grafo Recomendaciones', width=200,
                      fg_color='#8B4513', hover_color='#A0522D',
                      command=self._mostrar_grafo).pack(side='right', padx=5)

        container = ctk.CTkFrame(self, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=25, pady=10)
        container.grid_columnconfigure(0, weight=3)
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(container, fg_color='#16213e', corner_radius=12,
                            border_width=1, border_color='#2a2a4a')
        left.grid(row=0, column=0, sticky='nsew', padx=5)

        ctk.CTkLabel(left, text='Lista de Clientes',
                     font=ctk.CTkFont(size=16, weight='bold')).pack(pady=(12, 8))

        self._tabla_frame = ctk.CTkScrollableFrame(left, fg_color='transparent', height=350)
        self._tabla_frame.pack(fill='both', expand=True, padx=10, pady=5)

        right = ctk.CTkFrame(container, fg_color='#16213e', corner_radius=12,
                             border_width=1, border_color='#2a2a4a')
        right.grid(row=0, column=1, sticky='nsew', padx=5)

        ctk.CTkLabel(right, text='🏆 Cliente Estrella',
                     font=ctk.CTkFont(size=16, weight='bold')).pack(pady=(12, 8))

        self._top_frame = ctk.CTkScrollableFrame(right, fg_color='transparent')
        self._top_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self._cargar()

    def on_activate(self):
        self._cargar()

    def _cargar(self):
        self._clientes = self.ctrl.listar()
        self._renderizar_tabla()
        self._renderizar_top()

    def _renderizar_tabla(self):
        for w in self._tabla_frame.winfo_children():
            w.destroy()

        header = ctk.CTkFrame(self._tabla_frame, fg_color='#0d1b2a', corner_radius=8)
        header.pack(fill='x', pady=(0, 5))
        for col, w in [('#', 35), ('Nombre', 0), ('Teléfono', 110), ('Email', 0), ('Puntos', 65), ('', 100)]:
            ctk.CTkLabel(header, text=col, font=ctk.CTkFont(size=12, weight='bold'),
                         text_color='#2ECC71').pack(side='left', padx=4, anchor='w')

        for c in self._clientes:
            bg = '#1a1a3e' if self._clientes.index(c) % 2 == 0 else 'transparent'
            row = ctk.CTkFrame(self._tabla_frame, fg_color=bg, corner_radius=6)
            row.pack(fill='x', pady=1)

            ctk.CTkLabel(row, text=str(c.id), width=35, font=ctk.CTkFont(size=12)).pack(side='left', padx=4)
            ctk.CTkLabel(row, text=c.nombre, font=ctk.CTkFont(size=12), anchor='w').pack(side='left', fill='x', expand=True, padx=4)
            ctk.CTkLabel(row, text=c.telefono, width=110, font=ctk.CTkFont(size=12)).pack(side='left', padx=4)
            ctk.CTkLabel(row, text=c.email, font=ctk.CTkFont(size=12)).pack(side='left', fill='x', expand=True, padx=4)
            ctk.CTkLabel(row, text=str(c.puntos), width=65, font=ctk.CTkFont(size=12), text_color='#F39C12').pack(side='left', padx=4)

            btn_frame = ctk.CTkFrame(row, fg_color='transparent', width=100)
            btn_frame.pack(side='right', padx=4)
            btn_frame.pack_propagate(False)
            ctk.CTkButton(btn_frame, text='✏️', width=35, height=26,
                          command=lambda cid=c.id: self._editar(cid)).pack(side='left', padx=1)
            ctk.CTkButton(btn_frame, text='🗑️', width=35, height=26, fg_color='#922B21',
                          command=lambda cid=c.id: self._eliminar(cid)).pack(side='left', padx=1)

    def _renderizar_top(self):
        for w in self._top_frame.winfo_children():
            w.destroy()
        ordenados = sorted(self._clientes, key=lambda c: c.puntos, reverse=True)[:5]
        if not ordenados:
            ctk.CTkLabel(self._top_frame, text='Sin clientes aún', text_color='#666').pack(pady=20)
            return
        for i, c in enumerate(ordenados, 1):
            medallas = {1: '🥇', 2: '🥈', 3: '🥉'}
            icon = medallas.get(i, f'{i}.')
            row = ctk.CTkFrame(self._top_frame, fg_color='#1a1a3e', corner_radius=8)
            row.pack(fill='x', pady=2)
            ctk.CTkLabel(row, text=icon, width=30, font=ctk.CTkFont(size=16)).pack(side='left', padx=5)
            ctk.CTkLabel(row, text=c.nombre, font=ctk.CTkFont(size=13), anchor='w').pack(side='left', fill='x', expand=True)
            ctk.CTkLabel(row, text=f'{c.puntos} pts', font=ctk.CTkFont(size=13), text_color='#F39C12').pack(side='right', padx=10)

    def _buscar(self):
        query = self.search_entry.get()
        self._clientes = self.ctrl.buscar(query) if query else self.ctrl.listar()
        self._renderizar_tabla()

    def _abrir_formulario(self, cliente=None):
        dialog = ctk.CTkToplevel(self)
        dialog.title('Editar Cliente' if cliente else 'Nuevo Cliente')
        dialog.geometry('400x350')
        dialog.transient(self)
        dialog.grab_set()

        frame = ctk.CTkFrame(dialog, fg_color='#16213e', corner_radius=12)
        frame.pack(fill='both', expand=True, padx=15, pady=15)

        ctk.CTkLabel(frame, text='Datos del Cliente',
                     font=ctk.CTkFont(size=18, weight='bold')).pack(pady=(10, 15))

        entries = {}
        for key, label in [('nombre', 'Nombre'), ('telefono', 'Teléfono'), ('email', 'Email')]:
            ctk.CTkLabel(frame, text=f'{label}:', font=ctk.CTkFont(size=13)).pack(anchor='w', padx=20, pady=(5, 2))
            entry = ctk.CTkEntry(frame)
            entry.pack(fill='x', padx=20)
            if cliente:
                entry.insert(0, str(getattr(cliente, key, '')))
            entries[key] = entry

        def guardar():
            c = Cliente(
                id=cliente.id if cliente else None,
                nombre=entries['nombre'].get(),
                telefono=entries['telefono'].get(),
                email=entries['email'].get()
            )
            self.ctrl.guardar(c)
            dialog.destroy()
            self._cargar()

        ctk.CTkButton(frame, text='Guardar', command=guardar).pack(pady=15)

    def _editar(self, id):
        c = self.ctrl.obtener_por_id(id)
        if c:
            self._abrir_formulario(c)

    def _eliminar(self, id):
        self.ctrl.eliminar(id)
        self._cargar()

    def _mostrar_grafo(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title('Grafo de Recomendaciones')
        dialog.geometry('780x620')
        dialog.transient(self)
        dialog.grab_set()

        scroll_main = ctk.CTkScrollableFrame(dialog, fg_color='#16213e', corner_radius=12)
        scroll_main.pack(fill='both', expand=True, padx=15, pady=15)

        ctk.CTkLabel(scroll_main, text='🔗 Grafo de Productos — Recomendación de Combos',
                     font=ctk.CTkFont(size=16, weight='bold')).pack(pady=(10, 5))

        # ── Explicación ──
        expl = ctk.CTkFrame(scroll_main, fg_color='#0d1b2a', corner_radius=10)
        expl.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(expl, text='¿Cómo funciona?',
                     font=ctk.CTkFont(size=13, weight='bold'), text_color='#F39C12').pack(anchor='w', padx=12, pady=(8, 2))
        ctk.CTkLabel(expl, text=(
            'Se construye un Grafo NO DIRIGIDO donde cada vértice es un producto.\n'
            'Se crea una arista entre dos productos cuando aparecen juntos en un mismo pedido.\n'
            'La Matriz de Adyacencia registra la cantidad de veces que cada par se compró junto.\n\n'
            '🔎 ¿Por qué se recomiendan? Porque históricamente los clientes que pidieron X '
            'también pidieron Y (relación basada en datos reales de ventas).\n\n'
            'BFS (Anchura): Explora productos relacionados nivel por nivel.\n'
            'DFS (Profundidad): Explora una cadena de relaciones hasta el final.'
        ), font=ctk.CTkFont(size=11), text_color='#CCCCCC', justify='left', wraplength=680).pack(padx=12, pady=(0, 8))

        grafo = self.ctrl.construir_grafo_recomendaciones()
        vertices = grafo.obtener_vertices()
        matriz = grafo.obtener_matriz()

        # ── Lista de productos ──
        ctk.CTkLabel(scroll_main, text=f'📌 Productos en el grafo ({len(vertices)}):',
                     font=ctk.CTkFont(size=13, weight='bold')).pack(anchor='w', padx=10, pady=(8, 2))
        prod_scroll = ctk.CTkScrollableFrame(scroll_main, height=70, fg_color='#0d1b2a', corner_radius=8)
        prod_scroll.pack(fill='x', padx=10, pady=3)
        for v in vertices:
            ctk.CTkLabel(prod_scroll, text=f'  • {v}', font=ctk.CTkFont(size=11),
                         anchor='w').pack(fill='x', padx=10)

        # ── Matriz de Adyacencia con tabla fija ──
        ctk.CTkLabel(scroll_main, text=f'📊 Matriz de Adyacencia ({len(vertices)}x{len(vertices)}):',
                     font=ctk.CTkFont(size=13, weight='bold')).pack(anchor='w', padx=10, pady=(8, 2))

        mat_container = ctk.CTkFrame(scroll_main, fg_color='#0d1b2a', corner_radius=8)
        mat_container.pack(fill='x', padx=10, pady=3)
        mat_scroll = ctk.CTkScrollableFrame(mat_container, fg_color='transparent', height=160)
        mat_scroll.pack(fill='x', padx=2, pady=2)

        n = len(vertices)
        cols = n + 1
        mat_scroll.grid_columnconfigure(tuple(range(cols)), weight=0, minsize=70)

        header_bg = '#1a3d2e'
        ctk.CTkLabel(mat_scroll, text='', width=70, fg_color=header_bg,
                      corner_radius=4).grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
        for j, v in enumerate(vertices):
            display = v[:6] + '..' if len(v) > 6 else v
            lbl = ctk.CTkLabel(mat_scroll, text=display, width=70, font=ctk.CTkFont(size=10, weight='bold'),
                               fg_color=header_bg, corner_radius=4)
            lbl.grid(row=0, column=j + 1, sticky='nsew', padx=1, pady=1)

        for i, v in enumerate(vertices):
            display = v[:6] + '..' if len(v) > 6 else v
            bg_row = '#1a1a3e' if i % 2 == 0 else '#0d1b2a'
            lbl = ctk.CTkLabel(mat_scroll, text=display, width=70, font=ctk.CTkFont(size=10, weight='bold'),
                               fg_color=bg_row, corner_radius=4)
            lbl.grid(row=i + 1, column=0, sticky='nsew', padx=1, pady=1)
            for j in range(n):
                val = matriz[i][j]
                color = '#2ECC71' if val else '#444'
                cell = ctk.CTkLabel(mat_scroll, text=str(val), width=70, font=ctk.CTkFont(size=10),
                                    fg_color=bg_row, text_color=color, corner_radius=4)
                cell.grid(row=i + 1, column=j + 1, sticky='nsew', padx=1, pady=1)

        # ── BFS / DFS ──
        ctk.CTkLabel(scroll_main, text=f'🌐 BFS desde "{vertices[0]}": {grafo.bfs(vertices[0]) if vertices else "N/A"}',
                     font=ctk.CTkFont(size=12), text_color='#2ECC71', wraplength=680).pack(anchor='w', padx=10, pady=(8, 2))
        ctk.CTkLabel(scroll_main, text=f'DFS desde "{vertices[0]}": {grafo.dfs(vertices[0]) if vertices else "N/A"}',
                     font=ctk.CTkFont(size=12), text_color='#3498DB', wraplength=680).pack(anchor='w', padx=10, pady=2)

        # ── Euleriano / Hamiltoniano ──
        if len(vertices) <= 6 and vertices:
            euler = grafo.es_euleriano()
            hamil = grafo.es_hamiltoniano()
            ctk.CTkLabel(scroll_main,
                         text=f'📌 Euleriano: {"Sí (recorre todas las aristas una vez)" if euler else "No"} | '
                              f'Hamiltoniano: {"Sí (recorre todos los vértices una vez)" if hamil else "No"}',
                         font=ctk.CTkFont(size=12), text_color='#F39C12', wraplength=680).pack(anchor='w', padx=10, pady=5)

        n_aristas = sum(sum(1 for v in fila if v != 0) for fila in matriz)
        ctk.CTkLabel(scroll_main, text=f'Aristas totales: {n_aristas} relaciones entre productos',
                     font=ctk.CTkFont(size=11), text_color='#888888').pack(anchor='w', padx=10, pady=(2, 8))
