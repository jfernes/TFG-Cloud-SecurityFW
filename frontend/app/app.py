from crypt import methods
import os

from black import Priority
from service import *
from flask import Flask, redirect, render_template, send_from_directory, url_for, request
from flask_login import LoginManager, login_manager, current_user, login_user, login_required, logout_user
from forms import *
from models import *

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)  # Para mantener la sesión

app.config['SECRET_KEY'] = 'qH1vprMjavek52cv7Lmfe1FoCexrrV8egFnB21jHhkuOHm8hJUe1hwn7pKEZQ1fioUzDb3sWcNK1pJVVIhyrgvFiIrceXpKJBFIn_i9-LTLBCc4cqaI3gjJJHU6kxuT8bnC7Ng'

@app.route('/images/<path:path>')
def serve_static(path):
    return send_from_directory('images', path)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    print("entro")
    if current_user.is_authenticated:
        print("aut")
        return redirect(url_for('index'))
    else:
        error = None
        form = LoginForm(request.form)
        print("validar")
        if request.method == "POST" and form.validate:
            print("validado")
            u = checkLogin(form.email.data, form.password.data)
            if u == None:
                error = 'Invalid Credentials. Please try again.'
            else:
                users.append(u)
                login_user(u, remember=form.remember_me.data)
                return redirect(url_for('index'))
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
        registered = registerUser(form.name.data, form.email.data, form.password.data)
        if registered:
            return redirect(url_for('login'))
        else:
            error = "The email is registered"
    
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
    app.run(debug=True,host='0.0.0.0')
    
    