# vistas/organizacion_vista.py
import streamlit as st

class VistaOrganizacion:
    @staticmethod
    def mostrar():
        st.header("📊 Reportes de Organización")
    
    @staticmethod
    def mostrar_pendientes(df):
        st.subheader("📋 Préstamos Pendientes")
        if not df.empty:
            st.dataframe(df[['libro', 'persona', 'fecha_prestamo']], use_container_width=True)
        else:
            st.info("No hay préstamos pendientes")
    
    @staticmethod
    def mostrar_culminados(df):
        st.subheader("✅ Préstamos Completados")
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No hay préstamos completados")