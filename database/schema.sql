CREATE TABLE IF NOT EXISTS producto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT DEFAULT '',
    precio REAL NOT NULL,
    categoria TEXT NOT NULL,
    stock INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cliente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT DEFAULT '',
    email TEXT DEFAULT '',
    puntos INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER REFERENCES cliente(id),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado TEXT DEFAULT 'en_cola',
    total REAL DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS detalle_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INTEGER REFERENCES pedido(id),
    id_producto INTEGER REFERENCES producto(id),
    cantidad INTEGER NOT NULL,
    subtotal REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS venta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INTEGER UNIQUE REFERENCES pedido(id),
    total REAL NOT NULL,
    metodo_pago TEXT DEFAULT 'efectivo',
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO producto (nombre, descripcion, precio, categoria, stock) VALUES
('Café Americano', 'Café negro tradicional', 5.00, 'Bebidas Calientes', 100),
('Café Latte', 'Café con leche vaporizada', 7.00, 'Bebidas Calientes', 80),
('Cappuccino', 'Café con espuma de leche y canela', 8.00, 'Bebidas Calientes', 80),
('Mocha', 'Café con chocolate y leche', 9.00, 'Bebidas Calientes', 60),
('Té Verde', 'Té verde natural', 4.00, 'Bebidas Calientes', 50),
('Chocolate Caliente', 'Chocolate caliente cremoso', 7.00, 'Bebidas Calientes', 70),
('Jugo de Naranja', 'Jugo natural de naranja', 6.00, 'Bebidas Frias', 50),
('Limonada Frozen', 'Limonada frozen natural', 7.00, 'Bebidas Frias', 50),
('Smoothie de Fresa', 'Smoothie de fresa con yogurt', 10.00, 'Bebidas Frias', 40),
('Sandwich de Pollo', 'Sandwich de pollo con verduras', 12.00, 'Comidas', 30),
('Sandwich Vegetal', 'Sandwich vegetariano con aguacate', 11.00, 'Comidas', 25),
('Croissant con Jamón', 'Croissant relleno de jamón y queso', 9.00, 'Comidas', 35),
('Cheesecake', 'Tarta de queso con frutos rojos', 10.00, 'Postres', 20),
('Brownie', 'Brownie de chocolate con nueces', 7.00, 'Postres', 25),
('Alfajor Artesanal', 'Alfajor de maicena con dulce de leche', 4.00, 'Postres', 40);
