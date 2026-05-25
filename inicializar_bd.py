import streamlit as st

st.title("Biblioteca")
usuario = st.text_input("Usuario")
contrasena = st.text_input("Contraseña", type="password")

if st.button("Ingresar"):
    if usuario == "admin" and contrasena == "1234":
        st.success("Bienvenido")
    else:
        st.error("Error")