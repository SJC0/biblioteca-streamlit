# vistas/login_vista.py
import streamlit as st

class VistaLogin:
    @staticmethod
    def mostrar():
        st.set_page_config(page_title="Biblioteca", layout="wide")
        
        # Logo
        try:
            st.image("logo.png", width=150)
        except:
            pass
        
        st.title("📚 Universidad de Cundinamarca - Biblioteca")
        st.subheader("Inicio de Sesión")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            usuario = st.text_input("Usuario")
            contrasena = st.text_input("Contraseña", type="password")
        
        return usuario, contrasena
    
    @staticmethod
    def error():
        st.error("❌ Credenciales incorrectas")