import mysql.connector
import os


def connectDB():
    connection = mysql.connector.connect(
        host = os.environ.get('SQL_SERVER'),
        user = "root",
        password = "root",
        database="secframework"
    )
    return connection


                
def createUser(name, email, pwdhash):
    connection = connectDB()
    cursor = connection.cursor()
    statement1 = "SELECT email FROM users"
    cursor.execute(statement1)
    emails = cursor.fetchall()
    for e in emails:
        if(e == email):
            return False
    statement2 = "INSERT INTO users (name, email, pwdhash) VALUES (%s, %s, %s)" 
    val = (name, email, pwdhash)
    cursor.execute(statement2, val)
    connection.commit()
    connection.close()
    return True
    
'''
def checkLogin(email, pwdhash):
    statement = ""
    cursor = connection.cursor()
'''
