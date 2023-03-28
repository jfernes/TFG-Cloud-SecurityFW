import os
from flask import Flask, redirect, render_template, send_from_directory, url_for, request, send_file
from flask_login import LoginManager, login_manager, current_user, login_user, login_required, logout_user
from forms import *
from models import *
from service import *
import sys
from werkzeug.utils import secure_filename

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app) 
app.config['SECRET_KEY'] = 'qH1vprMjavek52cv7Lmfe1FoCexrrV8egFnB21jHhkuOHm8hJUe1hwn7pKEZQ1fioUzDb3sWcNK1pJVVIhyrgvFiIrceXpKJBFIn_i9-LTLBCc4cqaI3gjJJHU6kxuT8bnC7Ng'
app.config['UPLOAD_FOLDER'] = '/tmp/'

@app.route('/images/<path:path>')
def serve_static(path):
    return send_from_directory('images', path)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ruta")
@login_required
def ruta():
    return render_template("ruta.html")


@app.route("/login/<rol>", methods=['GET', 'POST'])
def login(rol):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        error = None
        form = LoginForm(request.form)
        if request.method == "POST" and form.validate():
            user = loginUser(form.email.data, form.password.data)
            if user == None:
                error = 'Invalid Credentials. Please try again.'
               
            else:
                user.rol=rol
                if rol == "admin" and not isAdmin(user.id):
                    error = 'You are not an admin.'
                    return render_template('login.html', form=form, error=error)
                users.append(user)
                login_user(user)
                return redirect(url_for('ruta'))
    return render_template('login.html', form=form, error=error)

@app.route("/rol")
def rol():
    return render_template("rol.html")


@app.route("/logout")
@login_required
def logout():
    users.remove(current_user)
    '''for user in users:
        if current_user.id == user.id:
            users.remove(user)'''
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
            return redirect(url_for('rol'))
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
        
        f = request.files['file']
        filename = secure_filename(f.filename)
        # Guardamos el archivo en el directorio "Archivos PDF"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))        
        
        uploaded = uploadSSLA(current_user.email, f, app.config['UPLOAD_FOLDER'] + filename)
        if uploaded:
            return redirect(url_for('ssla'))
        else:
            error = 'Error uploading SSLA. Try again.'

    return render_template("upload-ssla.html", error=error, form=form)

@app.route("/create")
@login_required
def create_ssla():
    pass


@app.route("/ssla/delete/<id>")
@login_required
def delete_ssla(id):
    deleteSSLA(current_user.id, id)
    return redirect(url_for("ssla"))

@app.route('/ssla')
@login_required
def ssla():
    is_ssla = False
    sslas = getSSLAS(current_user.id)
    if(len(sslas) > 0):
        is_ssla = True
    return render_template("managessla.html", sslas=sslas, is_ssla=is_ssla)

@app.route("/ssla/<id>")
@login_required
def details(id):
    data = getSSLA(id)
    is_data = False
    if data != None:
        is_data = True
    return render_template("details.html", data=data, is_data=is_data)

@app.route("/ssla/download/<id>")
@login_required
def downloadSSLA(id):
    file = downloadSSLAfromDB(id)
    return send_file(file, as_attachment=True)
    


@app.route("/ssla/json/<id>")
@login_required
def viewJSON(id):
    data = json.dumps(getSSLA(id), indent=4)
    return render_template("json.html", data=data)

@app.route("/negotiate", methods=['GET','POST'])
@login_required
def negotiate():
    is_intents = False
    intents = getIntents()
    if(len(intents) > 0):
        is_intents = True
        
    if request.method == 'POST':
        providers = getProvidersByIntents(request.form.getlist("id"))
        is_providers = False
        sys.stderr.write(str(providers))
        if(len(providers) > 0):
            is_providers = True
        return render_template("providers.html", providers=providers, is_providers=is_providers)
    
    return render_template("negotiate.html", intents=intents, is_intents=is_intents)

@app.route("/ssla/contract/<sslaid>/<providerid>")
@login_required
def contract(sslaid, providerid):
    error = None
    created = createContract(sslaid, providerid, current_user.id)
    if created:
        return redirect(url_for("manage_contracts"))
    else:
        error = "Could not create the contract."
    return render_template("providers.html", error=error)
        
@app.route("/contracts")
@login_required
def manage_contracts():
    is_contract = False
    contracts = getContracts(current_user.id)
    if (len(contracts) > 0):
        is_contract = True
    return render_template("contracts.html", contracts=contracts, is_contract=is_contract)

 
@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == user_id:
            return user
    return None
    

if __name__ == '__main__':
    app.run()