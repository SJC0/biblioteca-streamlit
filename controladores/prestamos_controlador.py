# controladores/prestamos_controlador.py
from modelos.libro import Libro
from modelos.persona import Persona
from modelos.prestamo import Prestamo

class ControladorPrestamos:
    @staticmethod
    def libros_disponibles():
        return Libro.obtener_disponibles()
    
    @staticmethod
    def personas_registradas():
        return Persona.obtener_para_prestamo()
    
    @staticmethod
    def realizar_prestamo(libro_id, persona_id):
        if not libro_id or not persona_id:
            return False, "Seleccione libro y persona"
        Prestamo.crear_prestamo(libro_id, persona_id)
        return True, "Préstamo registrado"
    
    @staticmethod
    def prestamos_pendientes():
        return Prestamo.obtener_pendientes()
    
    @staticmethod
    def devolver_prestamo(prestamo_id, libro_id):
        if prestamo_id:
            exito = Prestamo.devolver_prestamo(prestamo_id)
            if exito:
                return True, "Devolución completada"
        return False, "Error al devolver"