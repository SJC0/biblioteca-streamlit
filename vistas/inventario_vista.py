# vistas/inventario_vista.py
import streamlit as st

class VistaInventario:
    @staticmethod
    def mostrar():
        st.header("📚 Inventario de Libros")
    
    @staticmethod
    def formulario_agregar():
        with st.expander("➕ Agregar nuevo libro"):
            titulo = st.text_input("Título")
            autor = st.text_input("Autor")
            isbn = st.text_input("ISBN")
            stock = st.number_input("Stock", min_value=0, step=1)
            enviado = st.button("Guardar libro")
            return titulo, autor, isbn, stock, enviado
    
    @staticmethod
    def mostrar_tabla(dataframe):
        st.dataframe(dataframe, use_container_width=True)
    
    @staticmethod
    def formulario_actualizar(libros):
        st.subheader("📦 Modificar existencias")
        if libros:
            seleccion = st.selectbox(
                "Selecciona un libro",
                libros,
                format_func=lambda x: f"{x['titulo']} (Stock: {x['stock']})"
            )
            nuevo_stock = st.number_input(
                "Nuevo stock",
                min_value=0,
                step=1,
                value=seleccion['stock']
            )
            actualizar = st.button("Actualizar stock")
            return seleccion['id'], nuevo_stock, actualizar
        else:
            st.info("No hay libros registrados")
            return None, None, False
    
    @staticmethod
    def mensaje(texto, es_error=False):
        if es_error:
            st.error(texto)
        else:
            st.success(texto)