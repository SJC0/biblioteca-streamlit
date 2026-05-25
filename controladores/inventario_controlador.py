# controladores/inventario_controlador.py
from modelos.libro import Libro

class ControladorInventario:
    @staticmethod
    def agregar_libro(titulo, autor, isbn, stock):
        if not titulo or not autor or not isbn:
            return False, "Faltan título, autor o ISBN"
        if Libro.existe_isbn(isbn):
            return False, "Ya existe un libro con ese ISBN"
        resultado = Libro.crear(titulo, autor, isbn, stock)
        if resultado:
            return True, "Libro agregado correctamente"
        return False, "Error al agregar el libro"
    
    @staticmethod
    def listar_libros():
        return Libro.obtener_todos()
    
    @staticmethod
    def modificar_stock(libro_id, nuevo_stock):
        if libro_id and nuevo_stock >= 0:
            Libro.actualizar_stock(libro_id, nuevo_stock)
            return True, "Stock actualizado"
        return False, "Datos inválidos"
    
    @staticmethod
    def libros_con_stock():
        """Devuelve una lista de diccionarios para usar en selectbox"""
        resultados = Libro.obtener_con_stock()
        # Convertir a lista de diccionarios con las claves correctas
        libros = []
        for row in resultados:
            libros.append({
                'id': row['id'],
                'titulo': row['titulo'],
                'stock': row['stock']
            })
        return libros