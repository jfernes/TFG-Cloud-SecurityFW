import mysql.connector
import os




                
def createUser(name, email, pwdhash):
    connection = mysql.connector.connect(
        host = os.environ.get('SQL_SERVER'),
        user = "root",
        password = "root",
    )
    cursor = connection.cursor()
    cursor.execute("USE secframework;")
    
    statement = "INSERT INTO users(name, email, pwdhash) VALUES ('pepe', 'asdf@gmail.com', '1234123');" 
    
    cursor.execute(statement)
    cursor.commit()
    cursor.execute("SHOW TABLES;")
    result = cursor.fetchall()
    for x in result:
        with open('a.txt', 'w') as f:
            f.write(x)
    cursor.close()
    
'''
def checkLogin(email, pwdhash):
    statement = ""
    cursor = connection.cursor()
'''
