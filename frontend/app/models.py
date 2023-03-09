from werkzeug.security import check_password_hash, generate_password_hash

users=[]

class SSLA():
    def __init__(self, id, filename, data):
        self.id = id
        self.filename = filename
        self.data = data 

class User():
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    @classmethod
    def check_password(self, hashed_password, password): #Hashed: dato almacenado en BBDD  / Password: clave en texto claro
        return check_password_hash(hashed_password, password)
        