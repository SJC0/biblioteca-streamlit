
from modelos.persona import Persona

class ControladorPersonas:
    @staticmethod
    def agregar_persona(nombre, apellido, documento):
        if not nombre or not apellido:
            return False, "Nombre y apellido son obligatorios"
        if Persona.existe_documento(documento):
            return False, "Documento ya registrado"
        resultado = Persona.crear(nombre, apellido, documento)
        if resultado:
            return True, "Persona agregada"
        return False, "Error al agregar persona"
    
    @staticmethod
    def listar_personas():
        return Persona.obtener_todas()