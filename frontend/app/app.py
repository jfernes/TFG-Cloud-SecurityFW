import os
from flask import Flask, redirect, render_template, send_from_directory, url_for, request
from flask_login import LoginManager, login_manager, current_user, login_user, login_required, logout_user
from forms import *
from models import *
from service import *
import sys

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app) 
app.config['SECRET_KEY'] = 'qH1vprMjavek52cv7Lmfe1FoCexrrV8egFnB21jHhkuOHm8hJUe1hwn7pKEZQ1fioUzDb3sWcNK1pJVVIhyrgvFiIrceXpKJBFIn_i9-LTLBCc4cqaI3gjJJHU6kxuT8bnC7Ng'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ruta")
@login_required
def ruta():
    return render_template("ruta.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        error = None
        form = LoginForm(request.form)
        if request.method == "POST" and form.validate():
            sys.stderr.write("valido form")
            user = loginUser(form.email.data, form.password.data)
            if user == None:
                error = 'Invalid Credentials. Please try again.'
               
            else:
                users.append(user)
                login_user(user)
                return redirect(url_for('ruta'))
    return render_template('login.html', form=form, error=error)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        registered = signup(form.email.data, form.password.data, form.name.data)
        if registered:
            return redirect(url_for('login'))
        else:
            error = "The email is registered."
    else: 
        '''
        for key, value in form.errors.items(): 
            sys.stderr.write('%s:%s\n' % (key, value))
        '''
    return render_template("register.html", form=form, error=error)



@app.route("/upload", methods=['GET','POST'])
@login_required
def upload_ssla():
    error = None
    form = SSLAForm()
    if request.method == 'POST':
        file = form.file.data
        filename = form.file.data.filename
        uploaded = uploadSSLA(current_user.id, file, filename)
        if uploaded:
            return redirect(url_for('ssla'))
        else:
            error = 'Error uploading SSLA. Try again.'

    return render_template("upload-ssla.html", error=error, form=form)


@app.route('/ssla')
@login_required
def ssla():
    is_ssla = False
    sslas = getSSLAS(current_user.id)
    if(len(sslas) > 0):
        is_ssla = True
    return render_template("managessla.html", sslas=sslas, is_ssla=is_ssla)
 
@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == user_id:
            return user
    return None
    

if __name__ == '__main__':
    app.run()