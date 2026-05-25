# app.py - Versión sin Firebase (usa SQLite)
import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import os

st.set_page_config(page_title="Biblioteca Universidad de Cundinamarca", layout="wide")

# ========== CONEXIÓN A BASE DE DATOS ==========
def get_db():
    """Conectar a SQLite (se crea automáticamente)"""
    conn = sqlite3.connect('biblioteca.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Crear tablas si no existen"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Crear tablas
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        rol TEXT NOT NULL
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS libros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        isbn TEXT UNIQUE NOT NULL,
        stock INTEGER NOT NULL
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS personas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        documento TEXT UNIQUE
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS prestamos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        libro_id INTEGER NOT NULL,
        persona_id INTEGER NOT NULL,
        fecha_prestamo TEXT NOT NULL,
        fecha_devolucion TEXT,
        estado TEXT NOT NULL,
        FOREIGN KEY(libro_id) REFERENCES libros(id),
        FOREIGN KEY(persona_id) REFERENCES personas(id)
    )''')
    
    # Insertar datos de ejemplo si no existen
    cursor.execute("INSERT OR IGNORE INTO usuarios VALUES (1, 'admin', '1234', 'bibliotecario')")
    cursor.execute("INSERT OR IGNORE INTO usuarios VALUES (2, 'socio', 'abcd', 'socio')")
    cursor.execute("INSERT OR IGNORE INTO libros VALUES (1, 'Cien años de soledad', 'Gabriel García Márquez', '9788437604947', 5)")
    cursor.execute("INSERT OR IGNORE INTO libros VALUES (2, 'El amor en los tiempos del cólera', 'Gabriel García Márquez', '9788437604954', 3)")
    cursor.execute("INSERT OR IGNORE INTO personas VALUES (1, 'Juan', 'Pérez', '12345678')")
    cursor.execute("INSERT OR IGNORE INTO personas VALUES (2, 'María', 'Gómez', '87654321')")
    
    conn.commit()
    conn.close()

# Inicializar la base de datos
init_db()

# ========== FUNCIONES DE LA BIBLIOTECA ==========
def verificar_usuario(username, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def obtener_libros():
    conn = get_db()
    df = pd.read_sql("SELECT id, titulo, autor, isbn, stock FROM libros", conn)
    conn.close()
    return df

def agregar_libro(titulo, autor, isbn, stock):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO libros (titulo, autor, isbn, stock) VALUES (?,?,?,?)", 
                      (titulo, autor, isbn, stock))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def actualizar_stock(libro_id, nuevo_stock):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE libros SET stock=? WHERE id=?", (nuevo_stock, libro_id))
    conn.commit()
    conn.close()

def obtener_personas():
    conn = get_db()
    df = pd.read_sql("SELECT id, nombre, apellido, documento FROM personas", conn)
    conn.close()
    return df

def agregar_persona(nombre, apellido, documento):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO personas (nombre, apellido, documento) VALUES (?,?,?)", 
                      (nombre, apellido, documento))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def obtener_prestamos_pendientes():
    conn = get_db()
    df = pd.read_sql("""
        SELECT p.id, l.titulo as libro, per.nombre || ' ' || per.apellido as persona, p.fecha_prestamo
        FROM prestamos p
        JOIN libros l ON p.libro_id = l.id
        JOIN personas per ON p.persona_id = per.id
        WHERE p.estado = 'pendiente'
    """, conn)
    conn.close()
    return df

def crear_prestamo(libro_id, persona_id):
    conn = get_db()
    cursor = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO prestamos (libro_id, persona_id, fecha_prestamo, estado) VALUES (?,?,?,'pendiente')",
                  (libro_id, persona_id, fecha))
    cursor.execute("UPDATE libros SET stock = stock - 1 WHERE id=?", (libro_id,))
    conn.commit()
    conn.close()

def devolver_prestamo(prestamo_id, libro_id):
    conn = get_db()
    cursor = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE prestamos SET estado='culminado', fecha_devolucion=? WHERE id=?", (fecha, prestamo_id))
    cursor.execute("UPDATE libros SET stock = stock + 1 WHERE id=?", (libro_id,))
    conn.commit()
    conn.close()

# ========== INTERFAZ DE USUARIO ==========
if 'logueado' not in st.session_state:
    st.session_state.logueado = False

if not st.session_state.logueado:
    st.title("📚 Universidad de Cundinamarca - Biblioteca")
    st.subheader("Inicio de Sesión")
    
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Ingresar"):
        user = verificar_usuario(username, password)
        if user:
            st.session_state.usuario = username
            st.session_state.rol = user['rol']
            st.session_state.logueado = True
            st.rerun()
        else:
            st.error("❌ Credenciales inválidas")
else:
    st.sidebar.title(f"👋 Hola {st.session_state.usuario}")
    st.sidebar.write(f"**Rol:** {st.session_state.rol}")
    
    if st.sidebar.button("🚪 Cerrar sesión"):
        st.session_state.logueado = False
        st.rerun()
    
    if st.session_state.rol == 'bibliotecario':
        menu = st.sidebar.selectbox("Menú", ["📚 Inventario", "📖 Préstamos", "👥 Personas", "📊 Organización"])
    else:
        menu = st.sidebar.selectbox("Menú", ["📚 Inventario"])
    
    if menu == "📚 Inventario":
        st.header("📚 Inventario de Libros")
        
        with st.expander("➕ Agregar nuevo libro"):
            titulo = st.text_input("Título")
            autor = st.text_input("Autor")
            isbn = st.text_input("ISBN")
            stock = st.number_input("Stock", min_value=0, step=1)
            if st.button("Guardar libro"):
                if titulo and autor and isbn:
                    if agregar_libro(titulo, autor, isbn, stock):
                        st.success("✅ Libro agregado")
                        st.rerun()
                    else:
                        st.error("❌ ISBN duplicado")
                else:
                    st.error("❌ Completa todos los campos")
        
        df_libros = obtener_libros()
        st.dataframe(df_libros, use_container_width=True)
        
        if not df_libros.empty:
            st.subheader("📦 Modificar existencias")
            libro_seleccionado = st.selectbox("Seleccionar libro", df_libros['id'].tolist(),
                                               format_func=lambda x: f"{df_libros[df_libros['id']==x]['titulo'].values[0]} (Stock: {df_libros[df_libros['id']==x]['stock'].values[0]})")
            nuevo_stock = st.number_input("Nuevo stock", min_value=0, step=1, 
                                          value=int(df_libros[df_libros['id']==libro_seleccionado]['stock'].values[0]))
            if st.button("Actualizar stock"):
                actualizar_stock(libro_seleccionado, nuevo_stock)
                st.success("✅ Stock actualizado")
                st.rerun()
    
    elif menu == "📖 Préstamos":
        st.header("📖 Gestión de Préstamos")
        
        with st.expander("🆕 Nuevo préstamo"):
            df_libros = obtener_libros()
            libros_disponibles = df_libros[df_libros['stock'] > 0]
            df_personas = obtener_personas()
            
            if not libros_disponibles.empty and not df_personas.empty:
                libro = st.selectbox("Libro", libros_disponibles['id'].tolist(),
                                     format_func=lambda x: f"{libros_disponibles[libros_disponibles['id']==x]['titulo'].values[0]}")
                persona = st.selectbox("Persona", df_personas['id'].tolist(),
                                       format_func=lambda x: f"{df_personas[df_personas['id']==x]['nombre'].values[0]} {df_personas[df_personas['id']==x]['apellido'].values[0]}")
                if st.button("Realizar préstamo"):
                    crear_prestamo(libro, persona)
                    st.success("✅ Préstamo registrado")
                    st.rerun()
            else:
                st.warning("No hay libros disponibles o personas")
        
        with st.expander("📤 Devolver libro"):
            df_pendientes = obtener_prestamos_pendientes()
            if not df_pendientes.empty:
                st.dataframe(df_pendientes, use_container_width=True)
                prestamo_seleccionado = st.selectbox("Seleccionar préstamo", df_pendientes['id'].tolist(),
                                                      format_func=lambda x: f"{df_pendientes[df_pendientes['id']==x]['persona'].values[0]} - {df_pendientes[df_pendientes['id']==x]['libro'].values[0]}")
                libro_id = df_pendientes[df_pendientes['id']==prestamo_seleccionado]['id'].values[0]
                if st.button("Confirmar devolución"):
                    devolver_prestamo(prestamo_seleccionado, libro_id)
                    st.success("✅ Devolución completada")
                    st.rerun()
            else:
                st.info("No hay préstamos pendientes")
    
    elif menu == "👥 Personas":
        st.header("👥 Gestión de Personas")
        
        with st.expander("➕ Agregar persona"):
            nombre = st.text_input("Nombre")
            apellido = st.text_input("Apellido")
            documento = st.text_input("Documento")
            if st.button("Guardar persona"):
                if nombre and apellido:
                    if agregar_persona(nombre, apellido, documento):
                        st.success("✅ Persona agregada")
                        st.rerun()
                    else:
                        st.error("❌ Documento duplicado")
                else:
                    st.error("❌ Nombre y apellido requeridos")
        
        df_personas = obtener_personas()
        st.dataframe(df_personas, use_container_width=True)
    
    elif menu == "📊 Organización":
        st.header("📊 Reportes")
        
        tab1, tab2 = st.tabs(["Préstamos Pendientes", "Libros más prestados"])
        with tab1:
            df_pendientes = obtener_prestamos_pendientes()
            if not df_pendientes.empty:
                st.dataframe(df_pendientes, use_container_width=True)
            else:
                st.info("No hay préstamos pendientes")
        with tab2:
            st.info("Estadísticas en desarrollo")