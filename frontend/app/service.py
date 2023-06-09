from fileinput import filename
import uuid
from models import Contract, User, SSLA, Intent
from werkzeug.security import generate_password_hash
from os import remove
import os
import mysql.connector
import sys
import xmltodict
import json
from sslagen import *
from evaluator import *

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
    
    sql = "INSERT INTO intent(id, sslaid, name, description, technology) VALUES (%s, %s, %s, %s, %s)"
    sqlsc = "INSERT INTO seccontrol(id, name, control_domain, description, intentid) VALUES(%s, %s, %s, %s, %s)"
    
    techs = []
    
    for item in data["wsag:AgreementOffer"]["wsag:ServiceDescriptionTerm"]["specs:capabilities"]["specs:capability"]:
        intentid = item["@id"]
        val = (intentid, sslaid, item["@name"], item["@description"], item["technology"])
        techs.append(item["technology"])
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
                
    if not processsc:
        techsclean = []
        for tech in techs:
            if tech not in techsclean:
                techsclean.append(tech)
        trust = getCVSS(techsclean)
        sqlupdt = "UPDATE ssla SET trust = %s WHERE id = %s"
        val =(trust, sslaid)        
        cursor.execute(sqlupdt, val)
        
    
        
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
        sql = """INSERT INTO ssla(id, filename, data, userid, trust) VALUES (%s, %s, %s, %s, %s)"""
        val = (sslaid, filename, bd, user_id, 0) #TO DO poner un campo al usuario para definir el id
        
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
    
    sql = """SELECT id, filename, data, userid, trust FROM ssla 
                WHERE userid = '{}'""".format(userid)
    
    cursor.execute(sql)
    result = cursor.fetchall()
    for elem in result:
        ssla = SSLA(elem[0], elem[1], elem[2], elem[3], elem[4])
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
        ssla = SSLA(result[0], result[1], result[2], result[3], 0)
        with open(ssla.filename, 'wb') as file:
            file.write(ssla.data)
        return ssla.filename
    return None

def getSSLA(sslaid):
    connection = connectDB()
    cursor = connection.cursor()
    
    sql = """SELECT id, filename, data, userid, trust FROM ssla 
                WHERE id = '{}'""".format(sslaid)
    
    cursor.execute(sql)
    result = cursor.fetchone()
    
    if result != None:
        ssla = SSLA(result[0], result[1], result[2], result[3], result[4])
        with open(ssla.filename, 'wb') as fd:   # binary mode
            fd.write(ssla.data)
            
        with open(ssla.filename, 'rb') as fd:
            js = xmltodict.parse(fd.read())
        
        jsond = json.dumps(js, indent=4)
        data = json.loads(jsond)
        return data      
        
    return None

def getObjectSSLA(sslaid):
    connection = connectDB()
    cursor = connection.cursor()
    
    sql = """SELECT id, filename, data, userid, trust FROM ssla 
                WHERE id = '{}'""".format(sslaid)
    
    cursor.execute(sql)
    result = cursor.fetchone()
    if result != None:
        ssla = SSLA(result[0], result[1], result[2], result[3], result[4])
        return ssla
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
    
    sql = """SELECT id, filename, data, userid, trust FROM ssla"""
    
    cursor.execute(sql)
    result = cursor.fetchall()
    for elem in result:
        ssla = SSLA(elem[0], elem[1], elem[2], elem[3], elem[4])
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

def createContract(contractid, providerid, consumerid, filename, data):
    connection = connectDB()
    cursor = connection.cursor()
    
    sql = """SELECT contractid, providerid, consumerid FROM contract
            WHERE contractid = %s and providerid = %s and consumerid = %s"""
    val = (contractid, providerid, consumerid)
    
    cursor.execute(sql,val)
    result = cursor.fetchone()
    
    if result == None:
        sql = "INSERT INTO contract(contractid, providerid, consumerid, filename, data) VALUES (%s, %s, %s, %s, %s)"
        val = (contractid, providerid, consumerid, filename, data)
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
    
    sql = """SELECT contractid, providerid, consumerid, filename, data FROM contract WHERE
            consumerid = '{}'""".format(consumerid)
    cursor.execute(sql)
    result = cursor.fetchall()
    for elem in result:
        contract = Contract(elem[0], elem[1], elem[2], elem[3], elem[4])
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
        resource_provider_zone, intents, techs, userid):
    xml = generateSSLA(agreement_id, ssla_name, service_provider, expiration_time,
        template_name, template_id, service_description_name,
        service_name, resource_provider_id, resource_provider_name, 
        resource_provider_zone, intents, techs)
    filename = '/tmp/' + userid + '_' + agreement_id + ".xml"
    
    with open(filename, 'w') as f:
        f.write(xml)
    
    return uploadSSLA(userid, filename, False)

def genContractSSLA(sslaid, customerid, providerid, intents, data):
    agid = data["wsag:AgreementOffer"]["@wsag:AgreementId"]
    sslaname = data["wsag:AgreementOffer"]["wsag:Name"]
    sp = data["wsag:AgreementOffer"]["wsag:Context"]["wsag:ServiceProvider"]
    exptime = data["wsag:AgreementOffer"]["wsag:Context"]["wsag:ExpirationTime"]
    tempname = data["wsag:AgreementOffer"]["wsag:Context"]["wsag:TemplateName"]
    tempid = data["wsag:AgreementOffer"]["wsag:Context"]["wsag:TemplateId"]
    sdname = data["wsag:AgreementOffer"]["wsag:ServiceDescriptionTerm"]["@wsag:Name"]
    sdservicename = data["wsag:AgreementOffer"]["wsag:ServiceDescriptionTerm"]["@wsag:ServiceName"]
    rpid = data["wsag:AgreementOffer"]["wsag:ServiceDescriptionTerm"]["specs:serviceDescription"]["specs:serviceResources"]["specs:resourcesProvider"]["@id"]
    rpname = data["wsag:AgreementOffer"]["wsag:ServiceDescriptionTerm"]["specs:serviceDescription"]["specs:serviceResources"]["specs:resourcesProvider"]["@name"]
    rpzone = data["wsag:AgreementOffer"]["wsag:ServiceDescriptionTerm"]["specs:serviceDescription"]["specs:serviceResources"]["specs:resourcesProvider"]["@zone"]
    
    connection = connectDB()
    cursor = connection.cursor()
    
    techs = {}
    
    for int in intents:
        sqlt = "SELECT technology FROM intent WHERE id = %s and sslaid = %s"
        val = (int, sslaid)
        cursor.execute(sqlt, val)
        result = cursor.fetchone()
        techs[int] = result[0]
    
    xml = generateSSLA(agid, sslaname, sp, exptime, tempname, tempid, sdname,
                       sdservicename, rpid, rpname, rpzone, intents, techs)
    
    contractid = str(uuid.uuid4())
    filename = "/tmp/"+ contractid + ".xml"
    
    with open(filename, 'w') as f:
        f.write(xml)    
    bd = convertToBinaryData(filename)
    return createContract(contractid, providerid, customerid, filename, bd)
    
    
def getContract(contractid):
    connection = connectDB()
    cursor = connection.cursor()
    
    sql = """SELECT contractid, providerid, consumerid, filename, data FROM contract 
                WHERE contractid = '{}'""".format(contractid)
    
    cursor.execute(sql)
    result = cursor.fetchone()
    
    if result != None:
        contract = Contract(result[0], result[1], result[2], result[3], result[4])
        with open(contract.filename, 'wb') as fd:   # binary mode
            fd.write(contract.data)
            
        with open(contract.filename, 'rb') as fd:
            js = xmltodict.parse(fd.read())
        
        jsond = json.dumps(js, indent=4)
        data = json.loads(jsond)
        return data      
        
    return None
    
def downloadContractfromDB(contractid):
    connection = connectDB()
    cursor = connection.cursor()
    
    sql = """SELECT contractid, providerid, consumerid, filename, data FROM contract 
                WHERE contractid = '{}'""".format(contractid)
    
    cursor.execute(sql)
    result = cursor.fetchone()
    
    if result != None:
        contract = Contract(result[0], result[1], result[2], result[3], result[4])
        with open(contract.filename, 'wb') as file:
            file.write(contract.data)
        return contract.filename
    return None
    
    