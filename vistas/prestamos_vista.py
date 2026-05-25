# vistas/prestamos_vista.py
import streamlit as st

class VistaPrestamos:
    @staticmethod
    def mostrar():
        st.header("📖 Gestión de Préstamos")
    
    @staticmethod
    def sin_permiso():
        st.info("No tienes permisos para gestionar préstamos")
        return True
    
    @staticmethod
    def formulario_prestamo(libros, personas):
        with st.expander("🆕 Nuevo préstamo"):
            if libros and personas:
                libro = st.selectbox("Libro", libros, format_func=lambda x: f"{x['id']} - {x['titulo']}")
                persona = st.selectbox("Persona", personas, format_func=lambda x: f"{x['id']} - {x['nombre']} {x['apellido']}")
                enviado = st.button("Realizar préstamo")
                return libro['id'], persona['id'], enviado
            else:
                st.warning("No hay libros disponibles o personas registradas")
                return None, None, False
    
    @staticmethod
    def formulario_devolucion(pendientes):
        with st.expander("📤 Devolver libro"):
            if pendientes is not None and not pendientes.empty:
                st.subheader("Préstamos pendientes")
                st.dataframe(pendientes[['libro', 'persona', 'fecha_prestamo']], use_container_width=True)
                
                opciones = pendientes.apply(
                    lambda fila: f"{fila['id']} - {fila['persona']} - {fila['libro']}",
                    axis=1
                )
                seleccion = st.selectbox("Seleccionar préstamo a devolver", opciones)
                prestamo_id = int(seleccion.split(" - ")[0])
                libro_id = pendientes[pendientes['id']==prestamo_id]['libro_id'].values[0]
                devolver = st.button("Confirmar devolución")
                return prestamo_id, libro_id, devolver
            else:
                st.info("No hay préstamos pendientes")
                return None, None, False
    
    @staticmethod
    def mensaje(texto, es_error=False):
        if es_error:
            st.error(texto)
        else:
            st.success(texto)