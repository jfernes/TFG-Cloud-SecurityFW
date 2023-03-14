from models import User, SSLA
from werkzeug.security import generate_password_hash
from os import remove
import os
import mysql.connector
import sys
import xmltodict
import json


def connectDB():
    connection = mysql.connector.connect(
        host=os.environ.get('SQL_SERVER'),
        user="root",
        password="root",
        database="secframework"
)
    return connection


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def getJson(filename):
    with open(filename, 'rb') as fd:
        js = xmltodict.parse(fd.read())
        return json.dumps(js)

def loginUser(email,password):
    # Establecer conexión con la base de datos
    connection = connectDB()
    cursor = connection.cursor()

    # Comprobar si el usuario existe en la base de datos.
    sql = """SELECT name, email, password FROM user 
    WHERE email = '{}'""".format(email)
    cursor.execute(sql)
    result = cursor.fetchone()

    # Comprobar resultado ejecución. Si no devuelve ninguna fila, usuario no registrado. Si devuelve un resultado, comprobar contraseña y devolver usuario.
    if result != None:
        if password == result[2]:
            u = User(result[1], result[1], result[2], result[0])
            return u
    else:
        return None

def signup(email, password, name):
    connection = connectDB()
    cursor = connection.cursor()
    # Comprobar si el usuario existe en la base de datos.
    sql = """SELECT name, email, password FROM user 
                        WHERE email = '{}'""".format(email)

    cursor.execute(sql)
    result = cursor.fetchone()

    # Comprobar resultado. Si no se encuentra, registrar.
    if result == None:
        
        sql = "INSERT INTO user(email, name, password) VALUES (%s, %s, %s)"
        val = (email, name, password)
        cursor.execute(sql, val)
        connection.commit()
        connection.close()
        return True
    else:
        return False

def uploadSSLA(user_id, file, filename):
    with open(filename, 'rb') as fd:
        js = xmltodict.parse(fd.read())
        
    jsond = json.dumps(js)
    data = json.loads(jsond)
    sys.stderr.write(data["wsag:AgreementOffer"]["@wsag:AgreementId"])
    sslaid = data["wsag:AgreementOffer"]["@wsag:AgreementId"]
    
    bd = convertToBinaryData(filename)
    
    connection = connectDB()
    cursor = connection.cursor()
    
    sql = """SELECT id, filename, data, userid FROM ssla 
                        WHERE id = '{}'""".format(filename)

    cursor.execute(sql)
    result = cursor.fetchone()

    # Comprobar resultado. Si no se encuentra, registrar.
    if result == None:
        sql = """INSERT INTO ssla(id, filename, data, userid) VALUES (%s, %s, %s, %s)"""
        val = (sslaid, filename, bd, user_id) #TO DO poner un campo al usuario para definir el id
        
        cursor.execute(sql, val)
        connection.commit()
        connection.close()
        remove(filename)
        return True
    else:
        remove(filename)
        return False

def deleteSSLA(userid, sslaid):
    connection = connectDB()
    cursor = connection.cursor()
    
    sql = "DELETE FROM ssla  WHERE id = %s AND userid=%s"
    val = (sslaid, userid)
    
    cursor.execute(sql, val)
    connection.commit()
    connection.close()
    


def getSSLAS(userid):
    sslas = []
    connection = connectDB()
    cursor = connection.cursor()
    
    sql = """SELECT id, filename, data, userid FROM ssla 
                WHERE userid = '{}'""".format(userid)
    
    cursor.execute(sql)
    result = cursor.fetchall()
    for elem in result:
        ssla = SSLA(elem[0], elem[1], elem[2], elem[3])
        sslas.append(ssla)
    
    return sslas