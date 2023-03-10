from werkzeug.security import check_password_hash
from flask_login import UserMixin

users=[]

class User(UserMixin):
    def __init__(self, id, email, password, name=""):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        
    def get_user(email):
        for user in users:
            if user.email == email:
                return user
            return None

    @classmethod
    def check_password(self, hashed_password, password): #Hashed: dato almacenado en BBDD  / Password: clave en texto claro
        return check_password_hash(hashed_password, password)
    
    #print(generate_password_hash("pwd"))

class SSLA():
    def __init__(self, id, filename, data):
        self.id = id
        self.filename = filename
        self.data = data 