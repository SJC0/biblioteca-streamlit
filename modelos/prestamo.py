# modelos/prestamo.py
from basedatos.gestor_bd import bd
from datetime import datetime
import pandas as pd
from modelos.libro import Libro

class Prestamo:
    @staticmethod
    def crear_prestamo(libro_id, persona_id):
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        consulta = """INSERT INTO prestamos (libro_id, persona_id, fecha_prestamo, estado) 
                      VALUES (?,?,?,'pendiente')"""
        prestamo_id = bd.ejecutar_insertar(consulta, (libro_id, persona_id, fecha_actual))
        
        # Reducir stock
        libro = Libro.obtener_por_id(libro_id)
        if libro:
            Libro.actualizar_stock(libro_id, libro['stock'] - 1)
        return prestamo_id
    
    @staticmethod
    def devolver_prestamo(prestamo_id):
        consulta_libro = "SELECT libro_id FROM prestamos WHERE id=?"
        resultado = bd.ejecutar_consulta(consulta_libro, (prestamo_id,))
        if not resultado:
            return False
        
        libro_id = resultado[0]['libro_id']
        fecha_devolucion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        consulta_update = "UPDATE prestamos SET estado='culminado', fecha_devolucion=? WHERE id=?"
        bd.ejecutar_actualizar(consulta_update, (fecha_devolucion, prestamo_id))
        
        # Aumentar stock
        libro = Libro.obtener_por_id(libro_id)
        if libro:
            Libro.actualizar_stock(libro_id, libro['stock'] + 1)
        return True
    
    @staticmethod
    def obtener_pendientes():
        consulta = """
            SELECT 
                p.id,
                l.titulo AS libro,
                per.nombre || ' ' || per.apellido AS persona,
                p.fecha_prestamo,
                l.id as libro_id
            FROM prestamos p
            JOIN libros l ON p.libro_id = l.id
            JOIN personas per ON p.persona_id = per.id
            WHERE p.estado = 'pendiente'
        """
        with bd.obtener_conexion() as conexion:
            return pd.read_sql(consulta, conexion)
    
    @staticmethod
    def obtener_culminados():
        consulta = """
            SELECT p.id, l.titulo, per.nombre||' '||per.apellido as persona, 
                   p.fecha_prestamo, p.fecha_devolucion
            FROM prestamos p 
            JOIN libros l ON p.libro_id=l.id
            JOIN personas per ON p.persona_id=per.id
            WHERE p.estado='culminado'
        """
        with bd.obtener_conexion() as conexion:
            return pd.read_sql(consulta, conexion)