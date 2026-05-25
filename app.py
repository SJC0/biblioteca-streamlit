
import streamlit as st
from controladores.autenticacion_controlador import ControladorAutenticacion
from controladores.inventario_controlador import ControladorInventario
from controladores.prestamos_controlador import ControladorPrestamos
from controladores.personas_controlador import ControladorPersonas
from controladores.organizacion_controlador import ControladorOrganizacion
from vistas.login_vista import VistaLogin
from vistas.inventario_vista import VistaInventario
from vistas.prestamos_vista import VistaPrestamos
from vistas.personas_vista import VistaPersonas
from vistas.organizacion_vista import VistaOrganizacion

# Configuración de la página
st.set_page_config(page_title="Biblioteca Universidad de Cundinamarca", layout="wide")

# Estilo página
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #e8f5e9;
        }
        .stButton > button {
            background-color: #4caf50;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 8px 20px;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #388e3c;
            color: white;
        }
        h1, h2, h3 {
            color: #2e7d32;
        }
        .stAlert[data-baseweb="notification"] {
            background-color: #c8e6c9;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# estado_sesión
if 'logueado' not in st.session_state:
    st.session_state.logueado = False

# login
if not st.session_state.logueado:
    usuario, contrasena = VistaLogin.mostrar()
    if st.button("Ingresar"):
        usuario_obj = ControladorAutenticacion.iniciar_sesion(usuario, contrasena)
        if usuario_obj:
            st.session_state.usuario_actual = usuario_obj
            st.session_state.logueado = True
            st.rerun()
        else:
            VistaLogin.error()

# APP
else:
    usuario_actual = st.session_state.usuario_actual
    
    # Barra lateral
    st.sidebar.title(f"Hola {usuario_actual.nombre_usuario}")
    st.sidebar.write(f"**Rol:** {usuario_actual.rol}")
    
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.logueado = False
        st.session_state.usuario_actual = None
        st.rerun()
    
    # Menú según rol
    menu = st.sidebar.selectbox("Menú", usuario_actual.obtener_menu())
    
    # Inventario

    if menu == "Inventario":
        VistaInventario.mostrar()
        
        # Agregar libro
        titulo, autor, isbn, stock, enviado = VistaInventario.formulario_agregar()
        if enviado:
            ok, msg = ControladorInventario.agregar_libro(titulo, autor, isbn, stock)
            VistaInventario.mensaje(msg, not ok)
            if ok:
                st.rerun()
        
        # Mostrar libros
        df = ControladorInventario.listar_libros()
        if df is not None and not df.empty:
            VistaInventario.mostrar_tabla(df)
        else:
            st.info("No hay libros registrados")
        
        # Actualizar stock
        libros = ControladorInventario.libros_con_stock()
        if libros and len(libros) > 0:
            libro_id, nuevo_stock, actualizar = VistaInventario.formulario_actualizar(libros)
            if actualizar and libro_id:
                ok, msg = ControladorInventario.modificar_stock(libro_id, nuevo_stock)
                VistaInventario.mensaje(msg, not ok)
                if ok:
                    st.rerun()
    
    # prestamos
    elif menu == "Préstamos":
        if not usuario_actual.puede_gestionar_prestamos():
            VistaPrestamos.sin_permiso()
        else:
            VistaPrestamos.mostrar()
            
            # Nuevo préstamo
            libros = ControladorPrestamos.libros_disponibles()
            personas = ControladorPrestamos.personas_registradas()
            libro_id, persona_id, enviado = VistaPrestamos.formulario_prestamo(libros, personas)
            if enviado and libro_id and persona_id:
                ok, msg = ControladorPrestamos.realizar_prestamo(libro_id, persona_id)
                VistaPrestamos.mensaje(msg, not ok)
                if ok:
                    st.rerun()
            
            # Devolución
            pendientes = ControladorPrestamos.prestamos_pendientes()
            prestamo_id, libro_id, devolver = VistaPrestamos.formulario_devolucion(pendientes)
            if devolver and prestamo_id:
                ok, msg = ControladorPrestamos.devolver_prestamo(prestamo_id, libro_id)
                VistaPrestamos.mensaje(msg, not ok)
                if ok:
                    st.rerun()
    
    #Personas
    elif menu == "Personas":
        if not usuario_actual.puede_gestionar_prestamos():
            VistaPersonas.sin_permiso()
        else:
            VistaPersonas.mostrar()
            
            nombre, apellido, documento, enviado = VistaPersonas.formulario_agregar()
            if enviado:
                ok, msg = ControladorPersonas.agregar_persona(nombre, apellido, documento)
                VistaPersonas.mensaje(msg, not ok)
                if ok:
                    st.rerun()
            
            df = ControladorPersonas.listar_personas()
            VistaPersonas.mostrar_tabla(df)
    
    # Organización
    elif menu == "Organización":
        VistaOrganizacion.mostrar()
        
        pendientes = ControladorOrganizacion.prestamos_pendientes()
        VistaOrganizacion.mostrar_pendientes(pendientes)
        
        culminados = ControladorOrganizacion.prestamos_culminados()
        VistaOrganizacion.mostrar_culminados(culminados)