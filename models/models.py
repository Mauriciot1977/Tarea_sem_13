from flask_login import UserMixin
from conexion.conexion import obtener_conexion


class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username


def get_by_id(user_id):
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, username FROM usuarios WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            print(f"DEBUG: Usuario encontrado: {user}")
            cursor.close()
            if user:
                return User(user[0], user[1])
            return None


        finally:
            cursor.close()
            conexion.close()