import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../../database/sachas.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), '../../database/schema.sql')


class Conexion:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._conectar()
        return cls._instance

    def _conectar(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute('PRAGMA foreign_keys = ON')
        self._inicializar_bd()

    def _inicializar_bd(self):
        with open(SCHEMA_PATH, 'r') as f:
            self.conn.executescript(f.read())
        self.conn.commit()

    def obtener_cursor(self):
        return self.conn.cursor()

    def ejecutar(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor

    def ejecutar_muchos(self, query, params_list):
        cursor = self.conn.cursor()
        cursor.executemany(query, params_list)
        self.conn.commit()
        return cursor

    def cerrar(self):
        if self.conn:
            self.conn.close()
            Conexion._instance = None