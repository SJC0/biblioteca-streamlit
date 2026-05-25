# basedatos/gestor_bd.py
import sqlite3
import os
from contextlib import contextmanager

class GestorBaseDatos:
    def __init__(self, ruta=None):
        if ruta is None:
            self.ruta = os.path.join(os.path.dirname(__file__), 'biblioteca.db')
        else:
            self.ruta = ruta
    
    @contextmanager
    def obtener_conexion(self):
        conexion = sqlite3.connect(self.ruta)
        conexion.row_factory = sqlite3.Row
        try:
            yield conexion
            conexion.commit()
        except Exception as e:
            conexion.rollback()
            raise e
        finally:
            conexion.close()
    
    def ejecutar_consulta(self, consulta, parametros=None):
        with self.obtener_conexion() as conexion:
            cursor = conexion.execute(consulta, parametros or [])
            return cursor.fetchall()
    
    def ejecutar_insertar(self, consulta, parametros=None):
        with self.obtener_conexion() as conexion:
            cursor = conexion.execute(consulta, parametros or [])
            return cursor.lastrowid
    
    def ejecutar_actualizar(self, consulta, parametros=None):
        with self.obtener_conexion() as conexion:
            cursor = conexion.execute(consulta, parametros or [])
            return cursor.rowcount

bd = GestorBaseDatos()

def inicializar_bd():
    """Crear tablas y datos iniciales"""
    with bd.obtener_conexion() as conn:
        # Tabla usuarios
        conn.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL
        )''')
        
        # Tabla libros
        conn.execute('''CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            isbn TEXT UNIQUE NOT NULL,
            stock INTEGER NOT NULL
        )''')
        
        # Tabla personas
        conn.execute('''CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            documento TEXT UNIQUE
        )''')
        
        # Tabla prestamos
        conn.execute('''CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            libro_id INTEGER NOT NULL,
            persona_id INTEGER NOT NULL,
            fecha_prestamo TEXT NOT NULL,
            fecha_devolucion TEXT,
            estado TEXT NOT NULL,
            FOREIGN KEY(libro_id) REFERENCES libros(id),
            FOREIGN KEY(persona_id) REFERENCES personas(id)
        )''')
        
        # Datos de ejemplo
        conn.execute("INSERT OR IGNORE INTO usuarios VALUES (1, 'admin', '1234', 'bibliotecario')")
        conn.execute("INSERT OR IGNORE INTO usuarios VALUES (2, 'socio', 'abcd', 'socio')")
        conn.execute("INSERT OR IGNORE INTO libros VALUES (1, 'Cien años de soledad', 'Gabriel García Márquez', '9788437604947', 5)")
        conn.execute("INSERT OR IGNORE INTO libros VALUES (2, 'El amor en los tiempos del cólera', 'Gabriel García Márquez', '9788437604954', 3)")
        conn.execute("INSERT OR IGNORE INTO personas VALUES (1, 'Juan', 'Pérez', '12345678')")
        conn.execute("INSERT OR IGNORE INTO personas VALUES (2, 'María', 'Gómez', '87654321')")

# Inicializar al importar
inicializar_bd()