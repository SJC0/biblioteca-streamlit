# vistas/personas_vista.py
import streamlit as st

class VistaPersonas:
    @staticmethod
    def mostrar():
        st.header("👥 Gestión de Personas")
    
    @staticmethod
    def sin_permiso():
        st.info("No tienes permisos para gestionar personas")
        return True
    
    @staticmethod
    def formulario_agregar():
        with st.expander("➕ Agregar persona"):
            nombre = st.text_input("Nombre")
            apellido = st.text_input("Apellido")
            documento = st.text_input("Documento (opcional)")
            enviado = st.button("Guardar persona")
            return nombre, apellido, documento, enviado
    
    @staticmethod
    def mostrar_tabla(dataframe):
        st.dataframe(dataframe, use_container_width=True)
    
    @staticmethod
    def mensaje(texto, es_error=False):
        if es_error:
            st.error(texto)
        else:
            st.success(texto)