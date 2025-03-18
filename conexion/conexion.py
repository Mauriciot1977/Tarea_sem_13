import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',  # Cambia si tu servidor MySQL no está en localhost
            user='root',  # Reemplaza con tu usuario de MySQL
            password='Mauricio1977',  # Reemplaza con tu contraseña de MySQL
            database='desarrollo_web',  # ⚠️ Revisa que el nombre esté bien escrito
            port=3307  # 📌 Configurar MySQL en el puerto 3307
        )

        if conexion.is_connected():
            print("✅ Conexión exitosa a la base de datos")
        return conexion

    except Error as e:
        print(f"❌ Error al conectar a MySQL: {e}")
        return None
