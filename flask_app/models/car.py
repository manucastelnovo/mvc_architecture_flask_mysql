from flask_app.config.mysqlconnection import connectToMySQL

class Car:
    def __init__(self,data):
        self.id = data['id']
        self.model= data['model']
        self.year = data['year']
        self.seller = data['seller']
        self.user_id=data['user_id']
        self.description = data['description'],
        self.price=data['price'],
        self.make=data['make']
    @classmethod
    def save(cls,data):
        query = "INSERT INTO cars (model,year,seller,user_id,description,price,make) VALUES (%(model)s,%(year)s,%(seller)s,%(user_id)s,%(description)s,%(price)s,%(make)s)"
        return connectToMySQL('holamundo').query_db(query,data)

    @classmethod
    def get_all(cls,data):
        query = "SELECT * FROM cars;"
        cars_from_db =  connectToMySQL('holamundo').query_db(query,data)
        cars =[]
        for b in cars_from_db:
            cars.append(cls(b))
            print(cars)
        return cars

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM cars WHERE cars.id = %(id)s;"
        car_from_db = connectToMySQL('holamundo').query_db(query,data)

        return cls(car_from_db[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE cars SET model=%(model)s, year=%(year)s, seller=%(seller)s, description=%(description)s WHERE id = %(id)s;"
        update=connectToMySQL('holamundo').query_db(query,data)
        print('dentro',update)
        return update
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM cars WHERE id = %(id)s;"
        return connectToMySQL('holamundo').query_db(query,data)


