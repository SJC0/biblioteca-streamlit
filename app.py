# app.py - Versión para Firebase/Firestore
import streamlit as st
from datetime import datetime
import pandas as pd
from firebase_config import db

st.set_page_config(page_title="Biblioteca Universidad de Cundinamarca", layout="wide")


def obtener_usuarios():
    """Obtener usuarios desde Firestore"""
    users_ref = db.collection('usuarios')
    docs = users_ref.stream()
    return {doc.id: doc.to_dict() for doc in docs}

def verificar_usuario(username, password):
    """Verificar credenciales"""
    users_ref = db.collection('usuarios')
    query = users_ref.where('username', '==', username).where('password', '==', password).limit(1)
    results = query.stream()
    for user in results:
        return user.to_dict()
    return None

def obtener_libros():
    """Obtener todos los libros"""
    libros_ref = db.collection('libros')
    docs = libros_ref.stream()
    libros = []
    for doc in docs:
        libro = doc.to_dict()
        libro['id'] = doc.id
        libros.append(libro)
    return pd.DataFrame(libros)

def agregar_libro(titulo, autor, isbn, stock):
    """Agregar un nuevo libro"""
    libros_ref = db.collection('libros')
    libros_ref.add({
        'titulo': titulo,
        'autor': autor,
        'isbn': isbn,
        'stock': stock
    })

def actualizar_stock(libro_id, nuevo_stock):
    """Actualizar stock de un libro"""
    libro_ref = db.collection('libros').document(libro_id)
    libro_ref.update({'stock': nuevo_stock})

def obtener_personas():
    """Obtener todas las personas"""
    personas_ref = db.collection('personas')
    docs = personas_ref.stream()
    personas = []
    for doc in docs:
        persona = doc.to_dict()
        persona['id'] = doc.id
        personas.append(persona)
    return pd.DataFrame(personas)

def agregar_persona(nombre, apellido, documento):
    """Agregar una nueva persona"""
    personas_ref = db.collection('personas')
    personas_ref.add({
        'nombre': nombre,
        'apellido': apellido,
        'documento': documento
    })

def obtener_prestamos_pendientes():
    """Obtener préstamos activos"""
    prestamos_ref = db.collection('prestamos').where('estado', '==', 'pendiente')
    docs = prestamos_ref.stream()
    prestamos = []
    for doc in docs:
        prestamo = doc.to_dict()
        prestamo['id'] = doc.id
        # Obtener datos del libro y persona
        libro = db.collection('libros').document(prestamo['libro_id']).get().to_dict()
        persona = db.collection('personas').document(prestamo['persona_id']).get().to_dict()
        prestamo['libro_titulo'] = libro['titulo'] if libro else 'Desconocido'
        prestamo['persona_nombre'] = f"{persona['nombre']} {persona['apellido']}" if persona else 'Desconocido'
        prestamos.append(prestamo)
    return pd.DataFrame(prestamos)

def crear_prestamo(libro_id, persona_id):
    """Crear un nuevo préstamo"""
    prestamos_ref = db.collection('prestamos')
    prestamos_ref.add({
        'libro_id': libro_id,
        'persona_id': persona_id,
        'fecha_prestamo': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'estado': 'pendiente'
    })
    # Reducir stock
    libro_ref = db.collection('libros').document(libro_id)
    libro = libro_ref.get().to_dict()
    libro_ref.update({'stock': libro['stock'] - 1})

def devolver_prestamo(prestamo_id, libro_id):
    """Devolver un libro"""
    prestamo_ref = db.collection('prestamos').document(prestamo_id)
    prestamo_ref.update({
        'estado': 'culminado',
        'fecha_devolucion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    # Aumentar stock
    libro_ref = db.collection('libros').document(libro_id)
    libro = libro_ref.get().to_dict()
    libro_ref.update({'stock': libro['stock'] + 1})

# datos ejemplo

def inicializar_datos_ejemplo():
    """Cargar datos de ejemplo si la base está vacía"""
    # Verificar si ya hay libros
    libros = list(db.collection('libros').limit(1).stream())
    if not libros:
        # Agregar libros de ejemplo
        libros_ejemplo = [
            {'titulo': 'Cien años de soledad', 'autor': 'Gabriel García Márquez', 'isbn': '9788437604947', 'stock': 5},
            {'titulo': 'El amor en los tiempos del cólera', 'autor': 'Gabriel García Márquez', 'isbn': '9788437604954', 'stock': 3},
            {'titulo': 'Don Quijote de la Mancha', 'autor': 'Miguel de Cervantes', 'isbn': '9788420412140', 'stock': 2}
        ]
        for libro in libros_ejemplo:
            db.collection('libros').add(libro)
        
        # Agregar personas de ejemplo
        personas_ejemplo = [
            {'nombre': 'Juan', 'apellido': 'Pérez', 'documento': '12345678'},
            {'nombre': 'María', 'apellido': 'Gómez', 'documento': '87654321'}
        ]
        for persona in personas_ejemplo:
            db.collection('personas').add(persona)
        
        # Agregar usuarios
        usuarios_ejemplo = [
            {'username': 'admin', 'password': '1234', 'rol': 'bibliotecario'},
            {'username': 'socio', 'password': 'abcd', 'rol': 'socio'}
        ]
        for usuario in usuarios_ejemplo:
            db.collection('usuarios').add(usuario)
        
        st.success("✅ Datos de ejemplo cargados en Firebase")

# UI


inicializar_datos_ejemplo()

# Estado de sesión
if 'logueado' not in st.session_state:
    st.session_state.logueado = False

# PANTALLA DE LOGIN
if not st.session_state.logueado:
    st.image("logo.png", width=150) if __import__("os").path.exists("logo.png") else None
    st.title("📚 Universidad de Cundinamarca - Biblioteca")
    st.subheader("Inicio de Sesión")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Ingresar", use_container_width=True):
            user = verificar_usuario(username, password)
            if user:
                st.session_state.usuario = username
                st.session_state.rol = user['rol']
                st.session_state.logueado = True
                st.rerun()
            else:
                st.error("❌ Credenciales inválidas")

# APLICACIÓN PRINCIPAL
else:
    # Menú lateral
    st.sidebar.title(f"👋 Hola {st.session_state.usuario}")
    st.sidebar.write(f"**Rol:** {st.session_state.rol}")
    
    if st.sidebar.button("🚪 Cerrar sesión", use_container_width=True):
        st.session_state.logueado = False
        st.rerun()
    
    # Menú según rol
    if st.session_state.rol == 'bibliotecario':
        menu = st.sidebar.selectbox("Menú", ["📚 Inventario", "📖 Préstamos", "👥 Personas", "📊 Organización"])
    else:
        menu = st.sidebar.selectbox("Menú", ["📚 Inventario"])
    
    # Inventario
    if menu == "📚 Inventario":
        st.header("📚 Inventario de Libros")
        
        # Agregar libro
        with st.expander("➕ Agregar nuevo libro"):
            titulo = st.text_input("Título")
            autor = st.text_input("Autor")
            isbn = st.text_input("ISBN")
            stock = st.number_input("Stock", min_value=0, step=1)
            
            if st.button("Guardar libro"):
                if titulo and autor and isbn:
                    agregar_libro(titulo, autor, isbn, stock)
                    st.success("✅ Libro agregado correctamente")
                    st.rerun()
                else:
                    st.error("❌ Completa todos los campos")
        
        # Mostrar libros
        df_libros = obtener_libros()
        if not df_libros.empty:
            st.dataframe(df_libros[['titulo', 'autor', 'isbn', 'stock']], use_container_width=True)
            
            # Modificar stock
            st.subheader("📦 Modificar existencias")
            libro_seleccionado = st.selectbox("Seleccionar libro", df_libros['id'].tolist(), 
                                               format_func=lambda x: f"{df_libros[df_libros['id']==x]['titulo'].values[0]} (Stock: {df_libros[df_libros['id']==x]['stock'].values[0]})")
            
            nuevo_stock = st.number_input("Nuevo stock", min_value=0, step=1, 
                                          value=int(df_libros[df_libros['id']==libro_seleccionado]['stock'].values[0]))
            
            if st.button("Actualizar stock"):
                actualizar_stock(libro_seleccionado, nuevo_stock)
                st.success("✅ Stock actualizado")
                st.rerun()
        else:
            st.info("No hay libros registrados")
    
    # Prestamos
    elif menu == "📖 Préstamos" and st.session_state.rol == 'bibliotecario':
        st.header("📖 Gestión de Préstamos")
        
        # Nuevo préstamo
        with st.expander("🆕 Nuevo préstamo"):
            # Obtener libros disponibles
            df_libros = obtener_libros()
            libros_disponibles = df_libros[df_libros['stock'] > 0]
            
            # Obtener personas
            df_personas = obtener_personas()
            
            if not libros_disponibles.empty and not df_personas.empty:
                libro = st.selectbox("Libro", libros_disponibles['id'].tolist(),
                                     format_func=lambda x: f"{libros_disponibles[libros_disponibles['id']==x]['titulo'].values[0]} (Stock: {libros_disponibles[libros_disponibles['id']==x]['stock'].values[0]})")
                persona = st.selectbox("Persona", df_personas['id'].tolist(),
                                       format_func=lambda x: f"{df_personas[df_personas['id']==x]['nombre'].values[0]} {df_personas[df_personas['id']==x]['apellido'].values[0]}")
                
                if st.button("Realizar préstamo"):
                    crear_prestamo(libro, persona)
                    st.success("✅ Préstamo registrado")
                    st.rerun()
            else:
                st.warning("No hay libros disponibles o personas registradas")
        
        # Devoluciones
        with st.expander("📤 Devolver libro"):
            df_pendientes = obtener_prestamos_pendientes()
            if not df_pendientes.empty:
                st.dataframe(df_pendientes[['libro_titulo', 'persona_nombre', 'fecha_prestamo']], use_container_width=True)
                
                prestamo_seleccionado = st.selectbox("Seleccionar préstamo a devolver", df_pendientes['id'].tolist(),
                                                      format_func=lambda x: f"{df_pendientes[df_pendientes['id']==x]['persona_nombre'].values[0]} - {df_pendientes[df_pendientes['id']==x]['libro_titulo'].values[0]}")
                
                if st.button("Confirmar devolución"):
                    libro_id = df_pendientes[df_pendientes['id']==prestamo_seleccionado]['libro_id'].values[0]
                    devolver_prestamo(prestamo_seleccionado, libro_id)
                    st.success("✅ Devolución completada")
                    st.rerun()
            else:
                st.info("No hay préstamos pendientes")
    
    # personas
    elif menu == "👥 Personas" and st.session_state.rol == 'bibliotecario':
        st.header("👥 Gestión de Personas")
        
        with st.expander("➕ Agregar persona"):
            nombre = st.text_input("Nombre")
            apellido = st.text_input("Apellido")
            documento = st.text_input("Documento (opcional)")
            
            if st.button("Guardar persona"):
                if nombre and apellido:
                    agregar_persona(nombre, apellido, documento)
                    st.success("✅ Persona agregada")
                    st.rerun()
                else:
                    st.error("❌ Nombre y apellido son obligatorios")
        
        df_personas = obtener_personas()
        if not df_personas.empty:
            st.dataframe(df_personas[['nombre', 'apellido', 'documento']], use_container_width=True)
        else:
            st.info("No hay personas registradas")
    
    # organización
    elif menu == "📊 Organización" and st.session_state.rol == 'bibliotecario':
        st.header("📊 Reportes de Organización")
        
        tab1, tab2 = st.tabs(["📋 Préstamos Pendientes", "✅ Préstamos Completados"])
        
        with tab1:
            df_pendientes = obtener_prestamos_pendientes()
            if not df_pendientes.empty:
                st.dataframe(df_pendientes[['libro_titulo', 'persona_nombre', 'fecha_prestamo']], use_container_width=True)
            else:
                st.info("No hay préstamos pendientes")
        
        with tab2:
            st.info("Módulo en construcción - próximamente")