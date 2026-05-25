
import streamlit as st

st.set_page_config(page_title="Test", layout="centered")

st.write("### Iniciando prueba...")

if st.button("Haz clic aquí"):
    st.write("¡El botón funciona!")

st.write("Fin de la prueba")