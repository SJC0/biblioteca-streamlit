
from modelos.prestamo import Prestamo

class ControladorOrganizacion:
    @staticmethod
    def prestamos_pendientes():
        return Prestamo.obtener_pendientes()
    
    @staticmethod
    def prestamos_culminados():
        return Prestamo.obtener_culminados()