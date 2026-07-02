import customtkinter as ctk
from view.menu_view import MenuView
from view.pedidos_view import PedidosView
from view.caja_view import CajaView
from view.clientes_view import ClientesView
from view.estructuras_view import EstructurasView


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Sachas Café - Sistema de Gestión')
        self.geometry('1280x800')
        self.minsize(1024, 650)

        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('green')

        self._sidebar_buttons = []
        self._views = {}
        self._current_view = None

        self._build_sidebar()
        self._build_main_area()

        self._show_view('menu')

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)

        logo_label = ctk.CTkLabel(
            self.sidebar, text='SACHAS\nCAFÉ',
            font=ctk.CTkFont(size=24, weight='bold'),
            text_color='#2ECC71'
        )
        logo_label.pack(pady=(30, 10))

        separator = ctk.CTkFrame(self.sidebar, height=2, fg_color='#2ECC71')
        separator.pack(fill='x', padx=20, pady=10)

        nav_items = [
            ('📋', 'Menú', 'menu'),
            ('🧾', 'Pedidos', 'pedidos'),
            ('💰', 'Caja', 'caja'),
            ('👥', 'Clientes', 'clientes'),
            ('🔬', 'Estructuras', 'estructuras'),
        ]

        for icon, label, view_name in nav_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=f'{icon}  {label}',
                anchor='w',
                fg_color='transparent',
                hover_color='#1a3d2e',
                text_color='#CCCCCC',
                font=ctk.CTkFont(size=14),
                command=lambda v=view_name: self._show_view(v)
            )
            btn.pack(fill='x', padx=10, pady=3)
            self._sidebar_buttons.append((btn, view_name))

        separator2 = ctk.CTkFrame(self.sidebar, height=2, fg_color='#2ECC71')
        separator2.pack(fill='x', padx=20, pady=(20, 10))

        version_label = ctk.CTkLabel(
            self.sidebar, text='v1.0 · Algoritmos y ED',
            font=ctk.CTkFont(size=11),
            text_color='#666666'
        )
        version_label.pack(side='bottom', pady=15)

    def _build_main_area(self):
        self.main_container = ctk.CTkFrame(self, fg_color='#1a1a2e', corner_radius=0)
        self.main_container.pack(side='right', fill='both', expand=True)

        self._views['menu'] = MenuView(self.main_container, self)
        self._views['pedidos'] = PedidosView(self.main_container, self)
        self._views['caja'] = CajaView(self.main_container, self)
        self._views['clientes'] = ClientesView(self.main_container, self)
        self._views['estructuras'] = EstructurasView(self.main_container, self)

    def _show_view(self, view_name):
        if self._current_view:
            self._views[self._current_view].pack_forget()
        self._views[view_name].pack(fill='both', expand=True)
        self._current_view = view_name
        for btn, name in self._sidebar_buttons:
            if name == view_name:
                btn.configure(fg_color='#1a3d2e', text_color='#2ECC71')
            else:
                btn.configure(fg_color='transparent', text_color='#CCCCCC')
        if hasattr(self._views[view_name], 'on_activate'):
            self._views[view_name].on_activate()