# modelos/usuario.py
from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, nombre_usuario, rol):
        self.nombre_usuario = nombre_usuario
        self.rol = rol
    
    @abstractmethod
    def obtener_menu(self):
        pass
    
    def puede_gestionar_prestamos(self):
        return False
    
    @classmethod
    def desde_fila_bd(cls, fila):
        if fila['rol'] == 'bibliotecario':
            return Bibliotecario(fila['username'], fila['rol'])
        else:
            return Socio(fila['username'], fila['rol'])

class Bibliotecario(Usuario):
    def obtener_menu(self):
        return ["Inventario", "Préstamos", "Personas", "Organización"]
    
    def puede_gestionar_prestamos(self):
        return True

class Socio(Usuario):
    def obtener_menu(self):
        return ["Inventario"]