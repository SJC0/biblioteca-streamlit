# modelos/persona.py
from basedatos.gestor_bd import bd
import pandas as pd

class Persona:
    @staticmethod
    def crear(nombre, apellido, documento):
        consulta = "INSERT INTO personas (nombre, apellido, documento) VALUES (?,?,?)"
        try:
            return bd.ejecutar_insertar(consulta, (nombre, apellido, documento))
        except:
            return None
    
    @staticmethod
    def obtener_todas():
        consulta = "SELECT id, nombre, apellido, documento FROM personas"
        with bd.obtener_conexion() as conexion:
            return pd.read_sql(consulta, conexion)
    
    @staticmethod
    def obtener_para_prestamo():
        consulta = "SELECT id, nombre, apellido FROM personas"
        return bd.ejecutar_consulta(consulta)
    
    @staticmethod
    def existe_documento(documento):
        if not documento:
            return False
        consulta = "SELECT COUNT(*) as contar FROM personas WHERE documento = ?"
        resultado = bd.ejecutar_consulta(consulta, (documento,))
        return resultado[0]['contar'] > 0 if resultado else False