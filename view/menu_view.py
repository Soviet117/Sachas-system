import customtkinter as ctk
from controller.producto_controller import ProductoController
from model.entities.producto import Producto


class MenuView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color='transparent')
        self.app = app
        self.ctrl = ProductoController()
        self._productos = []
        self._categoria_actual = 'Todas'

        label = ctk.CTkLabel(
            self, text='Gestión del Menú',
            font=ctk.CTkFont(size=28, weight='bold'), anchor='w'
        )
        label.pack(fill='x', padx=30, pady=(25, 5))

        sub = ctk.CTkLabel(
            self, text='Administra los productos y explora el árbol AVL del catálogo',
            font=ctk.CTkFont(size=14), text_color='#888888', anchor='w'
        )
        sub.pack(fill='x', padx=30, pady=(0, 15))

        toolbar = ctk.CTkFrame(self, fg_color='transparent')
        toolbar.pack(fill='x', padx=25, pady=5)

        self.search_entry = ctk.CTkEntry(toolbar, placeholder_text='Buscar producto...', width=250)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self._buscar())

        ctk.CTkButton(toolbar, text='+ Nuevo', width=100, command=self._abrir_formulario).pack(side='left', padx=5)

        self._cat_var = ctk.StringVar(value='Todas')
        self._cat_menu = ctk.CTkOptionMenu(toolbar, values=['Todas'], variable=self._cat_var, command=lambda x: self._filtrar())
        self._cat_menu.pack(side='left', padx=5)

        ctk.CTkButton(toolbar, text='Ver Árbol AVL', width=120, fg_color='#8B4513', hover_color='#A0522D',
                      command=self._mostrar_arbol).pack(side='right', padx=5)

        self._tabla_frame = ctk.CTkScrollableFrame(self, fg_color='#16213e', corner_radius=12,
                                                    border_width=1, border_color='#2a2a4a')
        self._tabla_frame.pack(fill='both', expand=True, padx=25, pady=10)

        self._cargar()

    def on_activate(self):
        self._cargar()

    def _cargar(self):
        self._productos = self.ctrl.listar()
        categorias = self.ctrl.listar_categorias()
        self._cat_menu.configure(values=['Todas'] + categorias)
        self._renderizar_tabla()

    def _renderizar_tabla(self):
        for w in self._tabla_frame.winfo_children():
            w.destroy()

        productos = self._productos
        if self._categoria_actual != 'Todas':
            productos = [p for p in productos if p.categoria == self._categoria_actual]

        header = ctk.CTkFrame(self._tabla_frame, fg_color='#0d1b2a', corner_radius=8, height=40)
        header.pack(fill='x', pady=(0, 5))
        for col, w in [('#', 40), ('Nombre', 0), ('Categoría', 120), ('Precio', 80), ('Stock', 60), ('', 140)]:
            ctk.CTkLabel(header, text=col, font=ctk.CTkFont(size=13, weight='bold'),
                         text_color='#2ECC71').pack(side='left', padx=5, anchor='w' if col else 'center')

        if not productos:
            ctk.CTkLabel(self._tabla_frame, text='Sin productos', text_color='#666').pack(pady=30)
            return

        for p in productos:
            bg = '#1a1a3e' if productos.index(p) % 2 == 0 else 'transparent'
            row = ctk.CTkFrame(self._tabla_frame, fg_color=bg, corner_radius=6)
            row.pack(fill='x', pady=1)

            ctk.CTkLabel(row, text=str(p.id), width=40, font=ctk.CTkFont(size=13)).pack(side='left', padx=5)
            ctk.CTkLabel(row, text=p.nombre, font=ctk.CTkFont(size=13), anchor='w').pack(side='left', fill='x', expand=True, padx=5)
            ctk.CTkLabel(row, text=p.categoria, width=120, font=ctk.CTkFont(size=13)).pack(side='left', padx=5)
            ctk.CTkLabel(row, text=f'S/{p.precio:.2f}', width=80, font=ctk.CTkFont(size=13), text_color='#2ECC71').pack(side='left', padx=5)
            ctk.CTkLabel(row, text=str(p.stock), width=60, font=ctk.CTkFont(size=13)).pack(side='left', padx=5)

            btn_frame = ctk.CTkFrame(row, fg_color='transparent', width=140)
            btn_frame.pack(side='right', padx=5)
            btn_frame.pack_propagate(False)
            ctk.CTkButton(btn_frame, text='✏️', width=40, height=28,
                          command=lambda pid=p.id: self._editar(pid)).pack(side='left', padx=2)
            ctk.CTkButton(btn_frame, text='🗑️', width=40, height=28, fg_color='#922B21',
                          command=lambda pid=p.id: self._eliminar(pid)).pack(side='left', padx=2)

    def _buscar(self):
        query = self.search_entry.get()
        if query:
            self._productos = self.ctrl.buscar(query)
        else:
            self._productos = self.ctrl.listar()
        self._renderizar_tabla()

    def _filtrar(self):
        self._categoria_actual = self._cat_var.get()
        self._renderizar_tabla()

    def _abrir_formulario(self, producto=None):
        dialog = ctk.CTkToplevel(self)
        dialog.title('Editar Producto' if producto else 'Nuevo Producto')
        dialog.geometry('450x420')
        dialog.transient(self)
        dialog.grab_set()

        frame = ctk.CTkFrame(dialog, fg_color='#16213e', corner_radius=12)
        frame.pack(fill='both', expand=True, padx=15, pady=15)

        ctk.CTkLabel(frame, text='Datos del Producto',
                     font=ctk.CTkFont(size=18, weight='bold')).pack(pady=(10, 15))

        entries = {}
        campos = [
            ('nombre', 'Nombre', True),
            ('descripcion', 'Descripción', False),
            ('precio', 'Precio (S/)', True),
            ('categoria', 'Categoría', True),
            ('stock', 'Stock', True),
        ]

        for key, label, required in campos:
            ctk.CTkLabel(frame, text=f'{label}{" *" if required else ""}:',
                         font=ctk.CTkFont(size=13)).pack(anchor='w', padx=20, pady=(8, 2))
            entry = ctk.CTkEntry(frame, placeholder_text=label)
            entry.pack(fill='x', padx=20)
            if producto:
                entry.insert(0, str(getattr(producto, key, '')))
            entries[key] = entry

        def guardar():
            try:
                data = {k: e.get() for k, e in entries.items()}
                if not data['nombre']:
                    return
                p = Producto(
                    id=producto.id if producto else None,
                    nombre=data['nombre'],
                    descripcion=data['descripcion'],
                    precio=float(data['precio']),
                    categoria=data['categoria'],
                    stock=int(data['stock'])
                )
                self.ctrl.guardar(p)
                dialog.destroy()
                self._cargar()
            except ValueError:
                pass

        ctk.CTkButton(frame, text='Guardar', command=guardar).pack(pady=15)

    def _editar(self, id):
        p = self.ctrl.obtener_por_id(id)
        if p:
            self._abrir_formulario(p)

    def _eliminar(self, id):
        self.ctrl.eliminar(id)
        self._cargar()

    def _mostrar_arbol(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title('Árbol AVL del Catálogo')
        dialog.geometry('800x600')
        dialog.transient(self)
        dialog.grab_set()

        import tkinter as tk

        frame = ctk.CTkFrame(dialog, fg_color='#16213e', corner_radius=12)
        frame.pack(fill='both', expand=True, padx=15, pady=15)

        ctk.CTkLabel(frame, text='Catálogo como Árbol AVL (ordenado por nombre)',
                     font=ctk.CTkFont(size=16, weight='bold')).pack(pady=(10, 5))
        ctk.CTkLabel(frame, text='Cada nodo es un producto · Búsqueda O(log n) · Auto-balanceable',
                     font=ctk.CTkFont(size=11), text_color='#888').pack()

        arbol = self.ctrl.construir_arbol_catalogo()

        canvas_frame = ctk.CTkFrame(frame, fg_color='#0d1b2a', corner_radius=12)
        canvas_frame.pack(fill='both', expand=True, padx=10, pady=5)
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(canvas_frame, bg='#0d1b2a', highlightthickness=0)
        v_scroll = ctk.CTkScrollbar(canvas_frame, orientation='vertical', command=canvas.yview)
        h_scroll = ctk.CTkScrollbar(canvas_frame, orientation='horizontal', command=canvas.xview)
        canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        canvas.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')

        info = ctk.CTkFrame(frame, fg_color='transparent')
        info.pack(fill='x', padx=10, pady=2)

        if not arbol.raiz:
            canvas.create_text(350, 200, text='Catálogo vacío — agrega productos primero',
                               fill='#666666', font=('Arial', 14))
            return

        H_SPACING, V_SPACING, NODE_W, NODE_H = 148, 98, 108, 52
        positions = {}
        x_counter = [0]

        def inorder_layout(nodo, depth):
            if not nodo:
                return
            inorder_layout(nodo.izquierdo, depth + 1)
            x = x_counter[0] * H_SPACING + NODE_W // 2 + 40
            y = depth * V_SPACING + NODE_H // 2 + 35
            positions[nodo.clave] = (x, y, nodo)
            x_counter[0] += 1
            inorder_layout(nodo.derecho, depth + 1)

        inorder_layout(arbol.raiz, 0)

        total_nodes = x_counter[0]
        cw = max(total_nodes * H_SPACING + 120, 500)
        max_depth = max(((y - NODE_H // 2 - 35) // V_SPACING) for (x, y, n) in positions.values()) if positions else 0
        ch = max((max_depth + 1) * V_SPACING + 110, 250)
        canvas.configure(scrollregion=(0, 0, cw, ch))

        def draw_lines(nodo):
            if not nodo:
                return
            x, y, _ = positions.get(nodo.clave, (0, 0, None))
            if nodo.izquierdo and nodo.izquierdo.clave in positions:
                lx, ly, _ = positions[nodo.izquierdo.clave]
                canvas.create_line(x, y + NODE_H // 2, lx, ly - NODE_H // 2,
                                   fill='#2ECC71', width=2, smooth=True)
            if nodo.derecho and nodo.derecho.clave in positions:
                rx, ry, _ = positions[nodo.derecho.clave]
                canvas.create_line(x, y + NODE_H // 2, rx, ry - NODE_H // 2,
                                   fill='#2ECC71', width=2, smooth=True)
            draw_lines(nodo.izquierdo)
            draw_lines(nodo.derecho)

        draw_lines(arbol.raiz)

        for clave, (x, y, nodo) in positions.items():
            x0, y0 = x - NODE_W // 2, y - NODE_H // 2
            x1, y1 = x + NODE_W // 2, y + NODE_H // 2
            canvas.create_rectangle(x0 + 2, y0 + 2, x1 - 2, y1 - 2,
                                    fill='#1a3d2e', outline='#2ECC71', width=2)
            display = clave if len(clave) <= 14 else clave[:12] + '..'
            canvas.create_text(x, y - 8, text=display,
                               fill='#2ECC71', font=('Arial', 10, 'bold'))
            if hasattr(nodo.valor, 'precio'):
                canvas.create_text(x, y + 12, text=f'S/{nodo.valor.precio:.2f}',
                                   fill='#99CC99', font=('Arial', 9))

        inorden = arbol.inorden()
        preorden = arbol.preorden()
        postorden = arbol.postorden()

        def fmt(lista):
            if not lista:
                return '(vacío)'
            return ' → '.join(str(k) for k, v in lista)

        ctk.CTkLabel(info, text=f'📌 Inorden: {fmt(inorden)}',
                     font=ctk.CTkFont(size=11), text_color='#BBBBBB', wraplength=720).pack(anchor='w')
        ctk.CTkLabel(info, text=f'📌 Preorden: {fmt(preorden)}',
                     font=ctk.CTkFont(size=11), text_color='#BBBBBB', wraplength=720).pack(anchor='w')
        ctk.CTkLabel(info, text=f'📌 Postorden: {fmt(postorden)}',
                     font=ctk.CTkFont(size=11), text_color='#BBBBBB', wraplength=720).pack(anchor='w')

        ops = arbol.obtener_operaciones()
        if ops:
            ctk.CTkLabel(info, text='' + ' | '.join(ops[-5:]),
                         font=ctk.CTkFont(size=10), text_color='#F39C12', wraplength=720).pack(anchor='w')
