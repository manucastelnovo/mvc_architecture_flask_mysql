from flask_login import UserMixin

from flask_app.config.mysqlconnection import connectToMySQL

class User(UserMixin):
    

    def __init__(self,data):
        self.firstname= data['firstname']
        self.lastname = data['lastname']
        self.email = data['email']
        self.password = data['password']
        self.id = data['id']
        

    @classmethod
    def getUserById(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('holamundo').query_db(query, data)
        if len(result) == 0:
            return None
        return cls(result[0])

    @classmethod
    def getUserByEmail(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('holamundo').query_db(query,data)
        print(result)
        if len(result) == 0:
            return None
        return cls(result[0])

    @classmethod
    def createUser(cls,data):
        query = "INSERT INTO users (firstname,lastname,email,password) VALUES (%(firstname)s,%(lastname)s,%(email)s,%(password)s)"
        return connectToMySQL('holamundo').query_db(query,data)
    