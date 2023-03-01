from flask_app.controllers import cars
from flask_app import app



SECRET_KEY = '123123123'
app.config['SECRET_KEY'] = SECRET_KEY


if __name__ == '__main__':

    app.run(debug=True)