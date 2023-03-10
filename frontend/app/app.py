import os
from flask import Flask, redirect, render_template, send_from_directory, url_for, request
from flask_login import LoginManager, login_manager, current_user, login_user, login_required, logout_user
from forms import *
from models import *
from service import *

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)  # Para mantener la sesión 
app.config['SECRET_KEY'] = 'qH1vprMjavek52cv7Lmfe1FoCexrrV8egFnB21jHhkuOHm8hJUe1hwn7pKEZQ1fioUzDb3sWcNK1pJVVIhyrgvFiIrceXpKJBFIn_i9-LTLBCc4cqaI3gjJJHU6kxuT8bnC7Ng'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        error = None
        form = LoginForm(request.form)
        if request.method == "POST" and form.validate:
            logged_user = loginUser(form.email.data, form.password.data)
            if logged_user != None:
                if logged_user.password:    #En este valor tenemos True o False: en función si la contraseña introducida coincide con el hash
                    users.append(logged_user)
                    login_user(logged_user)
                    return redirect(url_for('index'))
                else:
                    error = 'Invalid Credentials. Please try again.'
            else:
                error= 'User not found.'
    return render_template('login.html', form=form, error=error)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    users.clear()
    return redirect(url_for('index'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate:
        registered = signup(form.email.data, form.password.data, form.name.data)
        if registered:
            return redirect(url_for('login'))
        else:
            error = "The email is registered. "
    return render_template("register.html", form=form, error=error)


@app.route("/upload", methods=['GET','POST'])
@login_required
def upload_ssla():
    form = sslaForm()
    if request.method == 'POST':
        file = form.file.data
        filename = form.file.data.filename
        
        #file.save(os.path.join('./', filename))

    return render_template("upload-ssla.html", form=form)

@app.route("/send", methods=['GET','POST'])
@login_required
def send_ssla():
    form = sslaForm()
    if request.method == 'POST':
        file = form.file.data
        filename = form.file.data

 
@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == user_id:
            return user
    return None
    

if __name__ == '__main__':
    app.run()
    