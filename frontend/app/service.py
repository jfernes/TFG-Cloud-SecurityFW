from fileinput import filename
from models import Contract, User, SSLA, Intent
from werkzeug.security import generate_password_hash
from os import remove
import os
import mysql.connector
import sys
import xmltodict
import json
from sslagen import *

def connectDB():
    connection = mysql.connector.connect(
        host=os.environ.get('SQL_SERVER'),
        user="root",
        password="root",
        database="secframework"
)
    return connection

def contains(big, small):
    for i in small:
        if i not in big:
            return False
    return True


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def processSSLA(sslaid, data, processsc):
    connection = connectDB()
    cursor = connection.cursor()
    
    sql = "INSERT INTO intent(id, sslaid, name, description) VALUES (%s, %s, %s, %s)"
    sqlsc = "INSERT INTO seccontrol(id, name, control_domain, description, intentid) VALUES(%s, %s, %s, %s, %s)"
    
    for item in data["wsag:AgreementOffer"]["wsag:ServiceDescriptionTerm"]["specs:capabilities"]["specs:capability"]:
        intentid = item["@id"]
        val = (intentid, sslaid, item["@name"], item["@description"])
        cursor.execute(sql, val)
        if processsc:
            if '@id' not in item["specs:controlFramework"]["specs:CCMsecurityControl"]:
                for elem in item["specs:controlFramework"]["specs:CCMsecurityControl"]:
                    val2 = (elem["@id"], elem["@name"], elem["@control_domain"], elem["ccm:description"], intentid)
                    cursor.execute(sqlsc, val2)
            else:
                item2 = item["specs:controlFramework"]["specs:CCMsecurityControl"]
                val2 = (item2["@id"], item2["@name"], item2["@control_domain"], item2["ccm:description"], intentid)
                cursor.execute(sqlsc, val2)
        
    connection.commit()
    connection.close()

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

def uploadSSLA(user_id, filename, processsc):
    with open(filename, 'rb') as fd:
        js = xmltodict.parse(fd.read())
        
    jsond = json.dumps(js)
    data = json.loads(jsond)
    
    sslaid = data["wsag:AgreementOffer"]["@wsag:AgreementId"]
    
    bd = convertToBinaryData(filename)
    
    connection = connectDB()
    cursor = connection.cursor()
    
    sql = """SELECT id, filename, data, userid FROM ssla 
                        WHERE id = '{}'""".format(sslaid)

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
        processSSLA(sslaid, data, processsc)
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

def downloadSSLAfromDB(sslaid):
    connection = connectDB()
    cursor = connection.cursor()
    
    sql = """SELECT id, filename, data, userid FROM ssla 
                WHERE id = '{}'""".format(sslaid)
    
    cursor.execute(sql)
    result = cursor.fetchone()
    
    if result != None:
        ssla = SSLA(result[0], result[1], result[2], result[3])
        with open(ssla.filename, 'wb') as file:
            file.write(ssla.data)
        return ssla.filename
    return None

def getSSLA(sslaid):
    connection = connectDB()
    cursor = connection.cursor()
    
    sql = """SELECT id, filename, data, userid FROM ssla 
                WHERE id = '{}'""".format(sslaid)
    
    cursor.execute(sql)
    result = cursor.fetchone()
    
    if result != None:
        ssla = SSLA(result[0], result[1], result[2], result[3])
        with open(ssla.filename, 'wb') as fd:   # binary mode
            fd.write(ssla.data)
            
        with open(ssla.filename, 'rb') as fd:
            js = xmltodict.parse(fd.read())
        
        jsond = json.dumps(js, indent=4)
        data = json.loads(jsond)
        return data      
        
    return None

def getIntents():
    intents = []
    connection = connectDB()
    cursor = connection.cursor()
    
    sql = """SELECT DISTINCT id, name, description FROM intent"""
    cursor.execute(sql)
    result = cursor.fetchall()
    for elem in result:
        intent = Intent(elem[0], "id", elem[1], elem[2])
        intents.append(intent)
    
    return intents

def getIntentsBySSLA(sslaid):
    intents=[]
    connection = connectDB()
    cursor = connection.cursor()
    
    sql = """SELECT id, sslaid, name, description FROM intent
        WHERE sslaid = '{}'""".format(sslaid)
    cursor.execute(sql)
    result = cursor.fetchall()
    for elem in result:
        intent = Intent(elem[0], elem[1], elem[2], elem[3])
        intents.append(intent)
    return intents

def getProvidersByIntents(intents):

    sslas = []
    providers = []
    connection = connectDB()
    cursor = connection.cursor()
    
    sql = """SELECT id, filename, data, userid FROM ssla"""
    
    cursor.execute(sql)
    result = cursor.fetchall()
    for elem in result:
        ssla = SSLA(elem[0], elem[1], elem[2], elem[3])
        sslas.append(ssla)
        
    connection.close()
    
    for ssla in sslas:
        if ssla.userid == "admin@um.es":
            continue
        ints = getIntentsBySSLA(ssla.id)
        ids = []
        for elem in ints:
            ids.append(elem.id)
        result = contains(ids, intents)
        if result:
            providers.append(ssla)
            
    return providers

def createContract(sslaid, providerid, consumerid):
    connection = connectDB()
    cursor = connection.cursor()
    
    sql = """SELECT sslaid, providerid, consumerid FROM contract
            WHERE sslaid = %s and providerid = %s and consumerid = %s"""
    val = (sslaid, providerid, consumerid)
    
    cursor.execute(sql,val)
    result = cursor.fetchone()
    
    if result == None:
        sql = "INSERT INTO contract(sslaid, providerid, consumerid) VALUES (%s, %s, %s)"
        val = (sslaid, providerid, consumerid)
        cursor.execute(sql, val)
        connection.commit()
        connection.close()
        return True
    else:
        return False
    
def getContracts(consumerid):
    contracts = []
    connection = connectDB()
    cursor = connection.cursor()
    
    sql = """SELECT sslaid, providerid, consumerid FROM contract WHERE
            consumerid = '{}'""".format(consumerid)
    cursor.execute(sql)
    result = cursor.fetchall()
    for elem in result:
        contract = Contract(elem[0], elem[1], elem[2])
        contracts.append(contract)
    return contracts

def isAdmin(userid):
    connection = connectDB()
    cursor = connection.cursor()
    
    sql = "SELECT id FROM admin WHERE id = '{}'".format(userid)
    
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        return False
    return True
        
def createSSLA(agreement_id, ssla_name, service_provider, expiration_time,
        template_name, template_id, service_description_name,
        service_name, resource_provider_id, resource_provider_name, 
        resource_provider_zone, intents, userid):
    xml = generateSSLA(agreement_id, ssla_name, service_provider, expiration_time,
        template_name, template_id, service_description_name,
        service_name, resource_provider_id, resource_provider_name, 
        resource_provider_zone, intents)
    filename = '/tmp/' + userid + '_' + agreement_id + ".xml"
    
    with open(filename, 'w') as f:
        f.write(xml)
    
    return uploadSSLA(userid, filename, False)