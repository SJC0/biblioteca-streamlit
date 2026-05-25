
from basedatos.gestor_bd import bd
from modelos.usuario import Usuario

class ControladorAutenticacion:
    @staticmethod
    def iniciar_sesion(usuario, contrasena):
        consulta = "SELECT * FROM usuarios WHERE username=? AND password=?"
        resultado = bd.ejecutar_consulta(consulta, (usuario, contrasena))
        if resultado:
            return Usuario.desde_fila_bd(resultado[0])
        return None