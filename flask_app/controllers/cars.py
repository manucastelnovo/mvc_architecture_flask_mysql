from flask import render_template,request,session,redirect,url_for
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# ------- MODELOS ---------------
from flask_app.models.car import Car
from flask_app.models.user import User

# ------- FORMULARIOS -----------
from flask_wtf import FlaskForm

# ------- VALIDADORES ---------------
from wtforms import StringField, EmailField, PasswordField, SubmitField,DecimalField
from wtforms.validators import InputRequired,Length,NumberRange

# ------- MANEJO DE SESSION ---------------
from flask_login import  login_user, LoginManager, login_required, logout_user, current_user


# ------- INSTANCIANDO FORMULARIOS ---------------
class RegisterForm(FlaskForm):
    firstname = StringField(validators=[InputRequired(),Length(min=3, max=20)])
    lastname = StringField(validators=[InputRequired(),Length(min=3, max=20)])
    email= EmailField(validators=[InputRequired(),Length(min=3, max=20)])
    password = PasswordField(validators=[InputRequired(),Length(min=8, max=20)])
    password2 = PasswordField(validators=[InputRequired(),Length(min=8, max=20)])
    id=StringField()
    submit = SubmitField('Register')

class RegisterCarForm(FlaskForm):
    model = StringField()
    year = StringField(validators=[InputRequired(),Length(min=3, max=5),NumberRange(min=1)])
    seller= StringField(validators=[InputRequired(),Length(min=3, max=20)])
    description= StringField(validators=[InputRequired(),Length(min=3, max=20)])
    price=DecimalField(validators=[InputRequired(),NumberRange(min=1)])
    make=StringField(validators=[InputRequired()])
    submit = SubmitField('Add')
    
class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(),Length(min=3, max=20)])
    password = PasswordField(validators=[InputRequired(),Length(min=8, max=20)])
    submit = SubmitField('login')

class editCarForm(FlaskForm):
    price = DecimalField(validators=[InputRequired(),NumberRange(min=1)])
    model=StringField(validators=[InputRequired()])
    make=StringField(validators=[InputRequired()])
    year= DecimalField(validators=[InputRequired(),NumberRange(min=1)])
    description= StringField(validators=[InputRequired()])
    submit=SubmitField()



# ------- INSTANCIANDO MANEJO DE SESSION ---------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'registerLogin'

@login_manager.user_loader
def load_user(user_id):
    data = {
        	"id" : user_id	
	}
    return User.getUserById(data)




# ------- RUTAS ---------------
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/show/<car_id>')
def detail_page(car_id):
    data = {
        'id': car_id
    }
    car=Car.get_one(data)
    print('soy el price',str(car.price))
    return render_template("details_page.html",burger=car)


@app.route('/edit_page/<car_id>', methods=['GET', 'POST'])
def edit_page(car_id):
    form=editCarForm()
    data = {
        'id': car_id,
        'price':form.price.data,
        'model': form.model.data,
        'make':form.make.data,
        'seller':current_user.firstname,
        'year': form.year.data,
        'description': form.description.data
    }
    if form.validate_on_submit and request.method=='POST':
         print('SOY UPDATE',Car.update(data))
         return redirect(url_for('dashboard'))
    return render_template("edit_page.html",form=form)


@app.route('/delete/<car_id>')
def delete(car_id):
    data = {
        'id': car_id,
    }
    Car.destroy(data)
    return redirect('/dashboard')


@app.route('/register', methods=['GET', 'POST'])
def registerLogin():
    formRegister = RegisterForm()
    formLogin= LoginForm()

    if formRegister.validate_on_submit() and request.method=='POST':
        hashed_password = bcrypt.generate_password_hash(formRegister.password.data).decode('utf-8')
        data = {
            "firstname" : formRegister.firstname.data,
            "lastname" : formRegister.lastname.data,
            "email" : formRegister.email.data,
            "password" : hashed_password,
            "id" : formRegister.id.data
        }
        User.createUser(data)
        user = User.getUserByEmail(data)
        login_user(user)
        return redirect(url_for('dashboard'))
    if formLogin.validate_on_submit():
        data={
            "email":formLogin.email.data
        }
        user= User.getUserByEmail(data)
        if user.email== formLogin.email.data and bcrypt.check_password_hash(user.password, formLogin.password.data):
            print('se valido pass y email')
            login_user(user)
            print(user.password)
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('registerLogin'))
    return render_template('register_login.html',formRegister=formRegister,formLogin=formLogin)



@app.route('/logout', methods=['GET','POST']) 
@login_required
def logout():
    logout_user()
    return redirect(url_for('registerLogin'))


@app.route('/dashboard', methods=['GET','POST']) 
@login_required
def dashboard(): 
    name=current_user.firstname
    data={"id":current_user.id}
    list_of_cars = Car.get_all(data)
    return render_template('dashboard.html',
                           name=name,
                           list_of_cars=list_of_cars)


@app.route('/addcar',methods=['GET','POST'])
@login_required
def addCar():
    form=RegisterCarForm()
    user=current_user
    print(user.id)
    if form.validate_on_submit and request.method=='POST':
        data={"model":form.model.data,
            "year":form.year.data,
            "seller":current_user.firstname,
            "user_id":user.id,
            "description":form.description.data,
            "price":form.price.data,
            "make":form.make.data}
        new_car=Car.save(data)
        print(new_car)
        return redirect(url_for('dashboard'))
    return render_template('new.html',form=form)