from models import User
from werkzeug.security import generate_password_hash
import os
import mysql.connector


def connectDB():
    connection = mysql.connector.connect(
        host=os.environ.get('SQL_SERVER'),
        user="root",
        password="root",
        database="secframework"
)
    return connection

def loginUser(email,password):
    # Establecer conexión con la base de datos
    connection = connectDB()
    cursor = connection.cursor()

    # Comprobar si el usuario existe en la base de datos.
    sql = """SELECT id, name, email, password FROM users 
    WHERE email = '{}'""".format(email)
    cursor.execute(sql)
    result = cursor.fetchone()

    # Comprobar resultado ejecución. Si no devuelve ninguna fila, usuario no registrado. Si devuelve un resultado, comprobar contraseña y devolver usuario.
    if result != None:
        # Los datos devueltos están en formato tupla. Puedo acceder a los campos en función de sus posiciones -> result[0]:id
        # Para el campo contraseña no lo devolvemos, solo almacenamos true/false si las contraseñas coinciden
        u = User(result[0], result[1], result[2], User.check_password(result[3], password))
        return u
    else:
        return None

def signup(email, password, name):
    connection = connectDB()
    cursor = connection.cursor()
    # Comprobar si el usuario existe en la base de datos.
    sql = sql = """SELECT id, name, email, password FROM users 
                        WHERE email = '{}'""".format(email)

    cursor.execute(sql)
    result = cursor.fetchone()

    # Comprobar resultado. Si no se encuentra, registrar.
    if result == None:
        sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        val = (name, email, generate_password_hash(password))
        cursor.execute(sql, val)
        connection.commit()
        return True
    else:
        return False
