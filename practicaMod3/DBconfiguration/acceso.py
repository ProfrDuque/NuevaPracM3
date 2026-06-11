import psycopg2
import getpass
import os  # Importar el módulo os para variables de entorno

# Configuración de la conexión a la base de datos (usando variables de entorno)
DB_HOST = os.getenv("DB_HOST", "localhost")  # Valor predeterminado si no se encuentra la variable
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "credenciales")
DB_USER = os.getenv("DB_USER", "Admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "p4ssw0rdDB")

def conectar_db():
    """Conecta a la base de datos PostgreSQL y retorna la conexión."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except psycopg2.Error as e:  # Capturar excepciones específicas de psycopg2
        print(f"Error de conexión a la base de datos: {e}")
        return None

def obtener_datos_usuario(username, password):
    """Consulta la base de datos para obtener los datos de un usuario a partir de sus credenciales."""
    conn = conectar_db()
    if not conn:
        return None  # Retornar None si la conexión falla

    try:
        cursor = conn.cursor()
        query = """
            SELECT u.id_usuario, u.nombre, u.correo, u.telefono, u.fecha_nacimiento
            FROM credenciales c
            JOIN usuarios u ON c.id_usuario = u.id_usuario
            WHERE c.username = %s AND c.password_hash = %s;
        """
        cursor.execute(query, (username, password))
        usuario = cursor.fetchone()

        if usuario:
            print("\nDatos del usuario encontrado:")
            print(f"ID: {usuario[0]}")
            print(f"Nombre: {usuario[1]}")
            print(f"Correo: {usuario[2]}")
            print(f"Teléfono: {usuario[3]}")
            print(f"Fecha de Nacimiento: {usuario[4]}")
        else:
            print("\nUsuario o contraseña incorrectos.")

        cursor.close()
        conn.close()
        return usuario  # Retornar los datos del usuario o None si no se encuentra
    except psycopg2.Error as e:  # Capturar excepciones específicas de psycopg2
        print(f"Error al consultar la base de datos: {e}")
        return None

if __name__ == "__main__":
    print("Inicio de sesión en la base de datos")
    username = input("Ingrese su usuario: ")
    password = getpass.getpass("Ingrese su contraseña: ")

    usuario = obtener_datos_usuario(username, password)

    # Puedes realizar acciones adicionales con los datos del usuario si se encuentra
    if usuario:
        print("\nInicio de sesión exitoso.")