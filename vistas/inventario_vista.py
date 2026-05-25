# vistas/inventario_vista.py
import streamlit as st

class VistaInventario:
    @staticmethod
    def mostrar():
        st.header("Inventario de Libros")
    
    @staticmethod
    def formulario_agregar():
        with st.expander("Agregar nuevo libro"):
            titulo = st.text_input("Título")
            autor = st.text_input("Autor")
            isbn = st.text_input("ISBN")
            stock = st.number_input("Stock", min_value=0, step=1)
            enviado = st.button("Guardar libro")
            return titulo, autor, isbn, stock, enviado
    
    @staticmethod
    def mostrar_tabla(dataframe):
        if dataframe is not None and not dataframe.empty:
            st.dataframe(dataframe, use_container_width=True)
        else:
            st.info("No hay libros registrados")
    
    @staticmethod
    def formulario_actualizar(libros):
        st.subheader("Modificar existencias")
        if libros and len(libros) > 0:
            # Crear opciones para el selectbox
            opciones = {f"{libro['titulo']} (Stock: {libro['stock']})": libro['id'] for libro in libros}
            
            seleccion_texto = st.selectbox(
                "Selecciona un libro",
                list(opciones.keys())
            )
            
            libro_id = opciones[seleccion_texto]
            libro_seleccionado = next((l for l in libros if l['id'] == libro_id), None)
            
            if libro_seleccionado:
                nuevo_stock = st.number_input(
                    "Nuevo stock",
                    min_value=0,
                    step=1,
                    value=int(libro_seleccionado['stock'])
                )
                actualizar = st.button("Actualizar stock")
                return libro_id, nuevo_stock, actualizar
            else:
                return None, None, False
        else:
            st.info("No hay libros registrados")
            return None, None, False
    
    @staticmethod
    def mensaje(texto, es_error=False):
        if es_error:
            st.error(texto)
        else:
            st.success(texto)