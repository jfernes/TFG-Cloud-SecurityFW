from connector import *

def registerUser(name, email, password):
    return createUser(name, email, password)
    

def checkLogin(email, password):
    print(email)
    print(password)
    return None