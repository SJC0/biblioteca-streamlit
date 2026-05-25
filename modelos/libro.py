# modelos/libro.py
from basedatos.gestor_bd import bd
import pandas as pd

class Libro:
    @staticmethod
    def crear(titulo, autor, isbn, stock):
        consulta = "INSERT INTO libros (titulo, autor, isbn, stock) VALUES (?,?,?,?)"
        try:
            return bd.ejecutar_insertar(consulta, (titulo, autor, isbn, stock))
        except:
            return None
    
    @staticmethod
    def obtener_todos():
        consulta = "SELECT id, titulo, autor, isbn, stock FROM libros"
        with bd.obtener_conexion() as conexion:
            return pd.read_sql(consulta, conexion)
    
    @staticmethod
    def actualizar_stock(libro_id, nuevo_stock):
        consulta = "UPDATE libros SET stock=? WHERE id=?"
        return bd.ejecutar_actualizar(consulta, (nuevo_stock, libro_id))
    
    @staticmethod
    def obtener_disponibles():
        consulta = "SELECT id, titulo, stock FROM libros WHERE stock > 0"
        return bd.ejecutar_consulta(consulta)
    
    @staticmethod
    def obtener_con_stock():
        consulta = "SELECT id, titulo, stock FROM libros"
        return bd.ejecutar_consulta(consulta)
    
    @staticmethod
    def existe_isbn(isbn):
        consulta = "SELECT COUNT(*) as contar FROM libros WHERE isbn = ?"
        resultado = bd.ejecutar_consulta(consulta, (isbn,))
        return resultado[0]['contar'] > 0 if resultado else False
    
    @staticmethod
    def obtener_por_id(libro_id):
        consulta = "SELECT stock FROM libros WHERE id = ?"
        resultado = bd.ejecutar_consulta(consulta, (libro_id,))
        return resultado[0] if resultado else None