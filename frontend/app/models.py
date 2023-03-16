from werkzeug.security import check_password_hash
from flask_login import UserMixin

users = []

class User(UserMixin):
    def __init__(self, id, email, password, name):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
    
    def get_user(email):
        for user in users:
            if user.email == email:
                return user
        
        return None
  

class SSLA():
    def __init__(self, id, filename, data, userid):
        self.id = id
        self.filename = filename
        self.data = data 
        self.userid = userid
        
class Intent():
    def __init__(self, id, sslaid, name, description):
        self.id = id
        self.sslaid = sslaid
        self.name = name
        self.description = description