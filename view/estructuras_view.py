import customtkinter as ctk
from structures.tad_lista import ListaEnlazada
from structures.tad_lista_doble import ListaDoblementeEnlazada
from structures.tad_pila import Pila
from structures.tad_cola import Cola
from structures.tad_arbol_avl import ArbolAVL
from structures.tad_grafo import Grafo


class EstructurasView(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color='transparent')
        self.app = app

        label = ctk.CTkLabel(
            self, text='🔬 Visualizador de Estructuras de Datos',
            font=ctk.CTkFont(size=28, weight='bold'), anchor='w'
        )
        label.pack(fill='x', padx=30, pady=(25, 5))

        sub = ctk.CTkLabel(
            self, text='Interactúa en vivo con las estructuras del sílabo — TAD, Listas, Pilas, Colas, Árboles y Grafos',
            font=ctk.CTkFont(size=14), text_color='#888888', anchor='w'
        )
        sub.pack(fill='x', padx=30, pady=(0, 15))

        tab = ctk.CTkTabview(self, fg_color='transparent')
        tab.pack(fill='both', expand=True, padx=25, pady=5)

        self._build_lista_tab(tab.add('📋 Lista Simple'))
        self._build_lista_doble_tab(tab.add('📋 Lista Doble'))
        self._build_pila_tab(tab.add('🥞 Pila (Stack)'))
        self._build_cola_tab(tab.add('🚶 Cola (Queue)'))
        self._build_arbol_tab(tab.add('🌳 Árbol AVL'))
        self._build_grafo_tab(tab.add('🔗 Grafo'))

    def _build_lista_tab(self, parent):
        self.lista = ListaEnlazada()
        ctk.CTkLabel(parent, text='Lista Enlazada Simple',
                     font=ctk.CTkFont(size=18, weight='bold')).pack(pady=(10, 5))
        ctk.CTkLabel(parent, text='Inserción y eliminación en O(1) al inicio, O(n) al final',
                     font=ctk.CTkFont(size=12), text_color='#888').pack()

        ctrl = ctk.CTkFrame(parent, fg_color='transparent')
        ctrl.pack(pady=10)

        self._lista_entry = ctk.CTkEntry(ctrl, placeholder_text='Valor', width=120)
        self._lista_entry.pack(side='left', padx=5)

        ctk.CTkButton(ctrl, text='Insertar Inicio', width=110,
                      command=lambda: self._lista_op('inicio')).pack(side='left', padx=3)
        ctk.CTkButton(ctrl, text='Insertar Final', width=110,
                      command=lambda: self._lista_op('final')).pack(side='left', padx=3)
        ctk.CTkButton(ctrl, text='Eliminar', width=90, fg_color='#922B21',
                      command=lambda: self._lista_op('eliminar')).pack(side='left', padx=3)
        ctk.CTkButton(ctrl, text='Vaciar', width=80, fg_color='#7B241C',
                      command=self._lista_vaciar).pack(side='left', padx=3)

        self._lista_display = ctk.CTkFrame(parent, fg_color='#0d1b2a', corner_radius=12, height=120)
        self._lista_display.pack(fill='x', padx=20, pady=10)
        self._lista_label = ctk.CTkLabel(self._lista_display, text='Lista vacía\n⬇\nNone',
                                         font=ctk.CTkFont(size=14), text_color='#666')
        self._lista_label.pack(expand=True)

        ctk.CTkLabel(parent, text='📍 Complejidad: Inserción Inicio O(1) · Inserción Final O(n) · Búsqueda O(n)',
                     font=ctk.CTkFont(size=11), text_color='#555').pack()

    def _lista_op(self, op):
        val = self._lista_entry.get().strip()
        if not val and op != 'eliminar':
            return
        if op == 'inicio':
            self.lista.insertar_inicio(val)
        elif op == 'final':
            self.lista.insertar_final(val)
        elif op == 'eliminar':
            v = self._lista_entry.get().strip()
            if v:
                self.lista.eliminar(v)
        self._actualizar_lista()
        self._lista_entry.delete(0, 'end')

    def _lista_vaciar(self):
        while not self.lista.esta_vacia():
            self.lista.eliminar(self.lista.cabeza.dato)
        self._actualizar_lista()

    def _actualizar_lista(self):
        if self.lista.esta_vacia():
            self._lista_label.configure(text='Lista vacía\n⬇\nNone', text_color='#666')
        else:
            nodos = self.lista.recorrer()
            texto = '  ➡  '.join(str(d) for d in nodos)
            texto += '\n⬇\nNone'
            self._lista_label.configure(text=texto, text_color='#2ECC71')

    def _build_lista_doble_tab(self, parent):
        self.lista_doble = ListaDoblementeEnlazada()
        ctk.CTkLabel(parent, text='Lista Doblemente Enlazada',
                     font=ctk.CTkFont(size=18, weight='bold')).pack(pady=(10, 5))
        ctk.CTkLabel(parent, text='Inserción y eliminación en O(1) en ambos extremos — recorrido bidireccional',
                     font=ctk.CTkFont(size=12), text_color='#888').pack()

        ctrl = ctk.CTkFrame(parent, fg_color='transparent')
        ctrl.pack(pady=10)

        self._ld_entry = ctk.CTkEntry(ctrl, placeholder_text='Valor', width=120)
        self._ld_entry.pack(side='left', padx=5)

        ctk.CTkButton(ctrl, text='Inicio', width=90,
                      command=lambda: self._ld_op('inicio')).pack(side='left', padx=3)
        ctk.CTkButton(ctrl, text='Final', width=90,
                      command=lambda: self._ld_op('final')).pack(side='left', padx=3)
        ctk.CTkButton(ctrl, text='Eliminar', width=90, fg_color='#922B21',
                      command=lambda: self._ld_op('eliminar')).pack(side='left', padx=3)
        ctk.CTkButton(ctrl, text='Vaciar', width=80, fg_color='#7B241C',
                      command=self._ld_vaciar).pack(side='left', padx=3)

        nav = ctk.CTkFrame(parent, fg_color='transparent')
        nav.pack(pady=5)
        ctk.CTkButton(nav, text='⬅️ Recorrer Atrás', width=140,
                      command=self._ld_recorrer_atras).pack(side='left', padx=5)
        ctk.CTkButton(nav, text='➡️ Recorrer Adelante', width=140,
                      command=self._ld_recorrer_adelante).pack(side='left', padx=5)

        self._ld_display = ctk.CTkFrame(parent, fg_color='#0d1b2a', corner_radius=12, height=140)
        self._ld_display.pack(fill='x', padx=20, pady=10)
        self._ld_label = ctk.CTkLabel(self._ld_display, text='Lista vacía\nNone  ⬌  None',
                                      font=ctk.CTkFont(size=14), text_color='#666')
        self._ld_label.pack(expand=True)

        self._ld_rec_label = ctk.CTkLabel(parent, text='',
                                          font=ctk.CTkFont(size=13), text_color='#3498DB')
        self._ld_rec_label.pack()

        ctk.CTkLabel(parent, text='📍 Complejidad: Inserción/Eliminación en extremos O(1) · Recorrido bidireccional',
                     font=ctk.CTkFont(size=11), text_color='#555').pack()

    def _ld_op(self, op):
        val = self._ld_entry.get().strip()
        if not val and op != 'eliminar':
            return
        if op == 'inicio':
            self.lista_doble.insertar_inicio(val)
        elif op == 'final':
            self.lista_doble.insertar_final(val)
        elif op == 'eliminar':
            v = self._ld_entry.get().strip()
            if v:
                self.lista_doble.eliminar(v)
        self._actualizar_ld()
        self._ld_entry.delete(0, 'end')

    def _ld_vaciar(self):
        while not self.lista_doble.esta_vacia():
            self.lista_doble.eliminar_primero()
        self._actualizar_ld()

    def _ld_recorrer_adelante(self):
        items = self.lista_doble.recorrer_adelante()
        if items:
            self._ld_rec_label.configure(text='➡️ ' + '  ↔  '.join(str(d) for d in items) + '  ➡️',
                                         text_color='#3498DB')
        else:
            self._ld_rec_label.configure(text='Lista vacía', text_color='#666')

    def _ld_recorrer_atras(self):
        items = self.lista_doble.recorrer_atras()
        if items:
            self._ld_rec_label.configure(text='⬅️ ' + '  ↔  '.join(str(d) for d in items) + '  ⬅️',
                                         text_color='#F39C12')
        else:
            self._ld_rec_label.configure(text='Lista vacía', text_color='#666')

    def _actualizar_ld(self):
        if self.lista_doble.esta_vacia():
            self._ld_label.configure(text='Lista vacía\nNone  ⬌  None', text_color='#666')
        else:
            items = self.lista_doble.recorrer_adelante()
            texto = '  ⬌  '.join(str(d) for d in items)
            texto += '\n⬆  Cabeza →  ' + str(self.lista_doble.cabeza.dato) + '  |  Cola →  ' + str(self.lista_doble.cola.dato) + '  ⬆'
            self._ld_label.configure(text=texto, text_color='#9B59B6')

    def _build_pila_tab(self, parent):
        self.pila = Pila()
        ctk.CTkLabel(parent, text='Pila (Stack) — LIFO',
                     font=ctk.CTkFont(size=18, weight='bold')).pack(pady=(10, 5))
        ctk.CTkLabel(parent, text='Último en entrar, primero en salir — usado para deshacer acciones',
                     font=ctk.CTkFont(size=12), text_color='#888').pack()

        ctrl = ctk.CTkFrame(parent, fg_color='transparent')
        ctrl.pack(pady=10)

        self._pila_entry = ctk.CTkEntry(ctrl, placeholder_text='Valor', width=120)
        self._pila_entry.pack(side='left', padx=5)

        ctk.CTkButton(ctrl, text='Push', width=80,
                      command=self._pila_push).pack(side='left', padx=3)
        ctk.CTkButton(ctrl, text='Pop', width=80,
                      command=self._pila_pop).pack(side='left', padx=3)
        ctk.CTkButton(ctrl, text='Peek', width=80,
                      command=self._pila_peek).pack(side='left', padx=3)
        ctk.CTkButton(ctrl, text='Vaciar', width=80, fg_color='#7B241C',
                      command=self._pila_vaciar).pack(side='left', padx=3)

        self._pila_display = ctk.CTkFrame(parent, fg_color='#0d1b2a', corner_radius=12, height=200)
        self._pila_display.pack(fill='x', padx=20, pady=10)
        self._pila_label = ctk.CTkLabel(self._pila_display, text='Pila vacía\n───\n|   |\n───',
                                        font=ctk.CTkFont(size=14), text_color='#666')
        self._pila_label.pack(expand=True)

        self._pila_info = ctk.CTkLabel(parent, text='Tamaño: 0',
                                       font=ctk.CTkFont(size=13), text_color='#888')
        self._pila_info.pack()

    def _pila_push(self):
        val = self._pila_entry.get().strip()
        if val:
            self.pila.push(val)
            self._actualizar_pila()
            self._pila_entry.delete(0, 'end')

    def _pila_pop(self):
        val = self.pila.pop()
        self._actualizar_pila()
        if val is not None:
            self._pila_info.configure(text=f'Pop → {val}')

    def _pila_peek(self):
        val = self.pila.peek()
        if val is not None:
            self._pila_info.configure(text=f'Cima → {val}')
        else:
            self._pila_info.configure(text='Pila vacía')

    def _pila_vaciar(self):
        self.pila.vaciar()
        self._actualizar_pila()

    def _actualizar_pila(self):
        if self.pila.esta_vacia():
            self._pila_label.configure(text='Pila vacía\n───\n|   |\n───', text_color='#666')
        else:
            items = self.pila.recorrer()
            lineas = ['───']
            for v in items:
                lineas.insert(0, f'| {v:^8} |')
            lineas.append('───')
            self._pila_label.configure(text='\n'.join(lineas), text_color='#F39C12')
        self._pila_info.configure(text=f'Tamaño: {self.pila.tamano()}')

    def _build_cola_tab(self, parent):
        self.cola = Cola()
        ctk.CTkLabel(parent, text='Cola (Queue) — FIFO',
                     font=ctk.CTkFont(size=18, weight='bold')).pack(pady=(10, 5))
        ctk.CTkLabel(parent, text='Primero en entrar, primero en salir — simula pedidos en cafetería',
                     font=ctk.CTkFont(size=12), text_color='#888').pack()

        ctrl = ctk.CTkFrame(parent, fg_color='transparent')
        ctrl.pack(pady=10)

        self._cola_entry = ctk.CTkEntry(ctrl, placeholder_text='Valor', width=120)
        self._cola_entry.pack(side='left', padx=5)

        ctk.CTkButton(ctrl, text='Enqueue', width=90,
                      command=self._cola_enqueue).pack(side='left', padx=3)
        ctk.CTkButton(ctrl, text='Dequeue', width=90,
                      command=self._cola_dequeue).pack(side='left', padx=3)
        ctk.CTkButton(ctrl, text='Peek', width=80,
                      command=self._cola_peek).pack(side='left', padx=3)
        ctk.CTkButton(ctrl, text='Vaciar', width=80, fg_color='#7B241C',
                      command=self._cola_vaciar).pack(side='left', padx=3)

        self._cola_display = ctk.CTkFrame(parent, fg_color='#0d1b2a', corner_radius=12, height=120)
        self._cola_display.pack(fill='x', padx=20, pady=10)
        self._cola_label = ctk.CTkLabel(self._cola_display,
                                        text='Cola vacía\n[ Frente  ←  Final ]',
                                        font=ctk.CTkFont(size=14), text_color='#666')
        self._cola_label.pack(expand=True)

        self._cola_info = ctk.CTkLabel(parent, text='Tamaño: 0',
                                       font=ctk.CTkFont(size=13), text_color='#888')
        self._cola_info.pack()

    def _cola_enqueue(self):
        val = self._cola_entry.get().strip()
        if val:
            self.cola.enqueue(val)
            self._actualizar_cola()
            self._cola_entry.delete(0, 'end')

    def _cola_dequeue(self):
        val = self.cola.dequeue()
        self._actualizar_cola()
        if val is not None:
            self._cola_info.configure(text=f'Dequeue → {val}')

    def _cola_peek(self):
        val = self.cola.peek()
        if val is not None:
            self._cola_info.configure(text=f'Frente → {val}')
        else:
            self._cola_info.configure(text='Cola vacía')

    def _cola_vaciar(self):
        self.cola.vaciar()
        self._actualizar_cola()

    def _actualizar_cola(self):
        if self.cola.esta_vacia():
            self._cola_label.configure(text='Cola vacía\n[ Frente  ←  Final ]', text_color='#666')
        else:
            items = self.cola.recorrer()
            flechas = '  ➡  '.join(str(v) for v in items)
            self._cola_label.configure(
                text=f'Frente → {flechas} ← Final\n[FIFO: primero en entrar, primero en salir]',
                text_color='#3498DB'
            )
        self._cola_info.configure(text=f'Tamaño: {self.cola.tamano()}')

    def _build_arbol_tab(self, parent):
        self.arbol = ArbolAVL()
        ctk.CTkLabel(parent, text='Árbol AVL (Auto-balanceable)',
                     font=ctk.CTkFont(size=18, weight='bold')).pack(pady=(10, 5))
        ctk.CTkLabel(parent, text='Se balancea automáticamente con rotaciones simples y dobles',
                     font=ctk.CTkFont(size=12), text_color='#888').pack()

        ctrl = ctk.CTkFrame(parent, fg_color='transparent')
        ctrl.pack(pady=10)

        self._arbol_entry = ctk.CTkEntry(ctrl, placeholder_text='Número (clave)', width=120)
        self._arbol_entry.pack(side='left', padx=5)
        ctk.CTkButton(ctrl, text='Insertar', width=80,
                      command=self._arbol_insertar).pack(side='left', padx=3)
        ctk.CTkButton(ctrl, text='Eliminar', width=80, fg_color='#922B21',
                      command=self._arbol_eliminar).pack(side='left', padx=3)

        insertar_ejemplos = ctk.CTkButton(ctrl, text='Cargar 10, 20, 30...', width=150,
                                          command=self._arbol_ejemplos)
        insertar_ejemplos.pack(side='left', padx=3)

        display = ctk.CTkFrame(parent, fg_color='#0d1b2a', corner_radius=12)
        display.pack(fill='both', expand=True, padx=20, pady=10)

        self._arbol_display = ctk.CTkScrollableFrame(display, fg_color='transparent')
        self._arbol_display.pack(fill='both', expand=True, padx=10, pady=10)

        info = ctk.CTkFrame(parent, fg_color='transparent')
        info.pack(fill='x', padx=20, pady=5)

        self._arbol_info = ctk.CTkLabel(info, text='📌 Inorden: (vacío)   |   Preorden: (vacío)   |   Postorden: (vacío)',
                                        font=ctk.CTkFont(size=12), text_color='#BBBBBB', wraplength=700)
        self._arbol_info.pack(anchor='w')

        self._arbol_ops_label = ctk.CTkLabel(info, text='',
                                             font=ctk.CTkFont(size=12), text_color='#F39C12', wraplength=700)
        self._arbol_ops_label.pack(anchor='w')

    def _arbol_insertar(self):
        val = self._arbol_entry.get().strip()
        if val:
            try:
                clave = int(val)
                self.arbol.insertar(clave, f'Valor-{clave}')
                self._actualizar_arbol()
                self._arbol_entry.delete(0, 'end')
            except ValueError:
                pass

    def _arbol_eliminar(self):
        val = self._arbol_entry.get().strip()
        if val:
            try:
                clave = int(val)
                self.arbol.eliminar(clave)
                self._actualizar_arbol()
                self._arbol_entry.delete(0, 'end')
            except ValueError:
                pass

    def _arbol_ejemplos(self):
        for v in [10, 20, 30, 5, 15, 25, 35, 3, 7, 12, 17]:
            self.arbol.insertar(v, f'Valor-{v}')
        self._actualizar_arbol()

    def _actualizar_arbol(self):
        for w in self._arbol_display.winfo_children():
            w.destroy()

        niveles = self.arbol.obtener_niveles()
        if not niveles:
            ctk.CTkLabel(self._arbol_display, text='🌳 Árbol vacío',
                         font=ctk.CTkFont(size=16), text_color='#666').pack(pady=20)
        else:
            for nivel, nodos in enumerate(niveles):
                frame_nivel = ctk.CTkFrame(self._arbol_display, fg_color='transparent')
                frame_nivel.pack(fill='x', pady=3)
                padding = '  ' * (len(niveles) - nivel)
                for clave, valor in nodos:
                    cell = ctk.CTkFrame(frame_nivel, fg_color='#1a3d2e', corner_radius=8,
                                        border_width=1, border_color='#2ECC71')
                    cell.pack(side='left', padx=6, pady=3)
                    ctk.CTkLabel(cell, text=str(clave), font=ctk.CTkFont(size=11, weight='bold'),
                                 text_color='#2ECC71').pack(padx=8, pady=3)
                ctk.CTkLabel(frame_nivel, text=f'  ← Nivel {nivel}',
                             font=ctk.CTkFont(size=10), text_color='#555').pack(side='left')

        inorden = self.arbol.inorden()
        preorden = self.arbol.preorden()
        postorden = self.arbol.postorden()

        def fmt(lista):
            if not lista:
                return '(vacío)'
            return ' → '.join(str(k) for k, v in lista)

        self._arbol_info.configure(
            text=f'📌 Inorden: {fmt(inorden)}   |   Preorden: {fmt(preorden)}   |   Postorden: {fmt(postorden)}'
        )

        ops = self.arbol.obtener_operaciones()
        if ops:
            texto = '🔄 ' + ' | '.join(ops[-5:])
            self._arbol_ops_label.configure(text=texto)

    def _build_grafo_tab(self, parent):
        self.grafo = Grafo(dirigido=False)
        ctk.CTkLabel(parent, text='Grafo — Matriz de Adyacencia',
                     font=ctk.CTkFont(size=18, weight='bold')).pack(pady=(10, 5))
        ctk.CTkLabel(parent, text='Representación de relaciones entre nodos usando matrices',
                     font=ctk.CTkFont(size=12), text_color='#888').pack()

        ctrl = ctk.CTkFrame(parent, fg_color='transparent')
        ctrl.pack(pady=10)

        self._grafo_origen = ctk.CTkEntry(ctrl, placeholder_text='Origen', width=90)
        self._grafo_origen.pack(side='left', padx=3)
        self._grafo_destino = ctk.CTkEntry(ctrl, placeholder_text='Destino', width=90)
        self._grafo_destino.pack(side='left', padx=3)

        ctk.CTkButton(ctrl, text='Agregar Arista', width=100,
                      command=self._grafo_agregar).pack(side='left', padx=3)
        ctk.CTkButton(ctrl, text='Eliminar Arista', width=100, fg_color='#922B21',
                      command=self._grafo_eliminar).pack(side='left', padx=3)
        ctk.CTkButton(ctrl, text='🌐 Cargar Ejemplo', width=130,
                      command=self._grafo_ejemplo).pack(side='left', padx=3)

        display = ctk.CTkFrame(parent, fg_color='#0d1b2a', corner_radius=12)
        display.pack(fill='both', expand=True, padx=20, pady=10)

        self._grafo_display = ctk.CTkScrollableFrame(display, fg_color='transparent')
        self._grafo_display.pack(fill='both', expand=True, padx=10, pady=10)

        info = ctk.CTkFrame(parent, fg_color='transparent')
        info.pack(fill='x', padx=20, pady=5)

        self._grafo_info = ctk.CTkLabel(info, text='Vértices: 0 | Aristas: 0 | BFS: (vacío) | DFS: (vacío)',
                                        font=ctk.CTkFont(size=12), text_color='#BBBBBB')
        self._grafo_info.pack(anchor='w')

    def _grafo_agregar(self):
        o = self._grafo_origen.get().strip()
        d = self._grafo_destino.get().strip()
        if o and d:
            self.grafo.agregar_arista(o, d, 1)
            self._actualizar_grafo()
            self._grafo_origen.delete(0, 'end')
            self._grafo_destino.delete(0, 'end')

    def _grafo_eliminar(self):
        o = self._grafo_origen.get().strip()
        d = self._grafo_destino.get().strip()
        if o and d:
            self.grafo.eliminar_arista(o, d)
            self._actualizar_grafo()

    def _grafo_ejemplo(self):
        for v in ['A', 'B', 'C', 'D', 'E']:
            self.grafo.agregar_vertice(v)
        self.grafo.agregar_arista('A', 'B', 1)
        self.grafo.agregar_arista('A', 'C', 1)
        self.grafo.agregar_arista('B', 'D', 1)
        self.grafo.agregar_arista('C', 'D', 1)
        self.grafo.agregar_arista('D', 'E', 1)
        self._actualizar_grafo()

    def _actualizar_grafo(self):
        for w in self._grafo_display.winfo_children():
            w.destroy()

        vertices = self.grafo.obtener_vertices()
        matriz = self.grafo.obtener_matriz()

        if not vertices:
            ctk.CTkLabel(self._grafo_display, text='Grafo vacío — agrega vértices con aristas',
                         font=ctk.CTkFont(size=14), text_color='#666').pack(pady=30)
        else:
            header = '     ' + ' '.join(f'{v:>4}' for v in vertices)
            ctk.CTkLabel(self._grafo_display, text=header,
                         font=ctk.CTkFont(size=10, weight='bold'),
                         text_color='#2ECC71').pack(anchor='w', padx=5)

            for i, v in enumerate(vertices):
                linea = f'{v:>4} ' + ' '.join(f'{matriz[i][j]:>4}' for j in range(len(vertices)))
                ctk.CTkLabel(self._grafo_display, text=linea,
                             font=ctk.CTkFont(size=10)).pack(anchor='w', padx=5)

        n_aristas = sum(sum(1 for v in fila if v != 0) for fila in matriz)
        bfs = self.grafo.bfs(vertices[0]) if vertices else []
        dfs = self.grafo.dfs(vertices[0]) if vertices else []

        self._grafo_info.configure(
            text=f'Vértices: {len(vertices)} | Aristas: {n_aristas} | BFS: {bfs} | DFS: {dfs}'
        )