from flask import Flask, render_template, send_from_directory, url_for

app = Flask(__name__)

@app.route('/images/<path:path>')
def serve_static(path):
    return send_from_directory('images', path)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("rol.html")

@app.route("/login/provider")
def provider_login():
    return render_template("login.html")

@app.route("/login/customer")
def customer_login():
    return render_template("login.html") 

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/upload")
def upload_ssla():
    return render_template("upload-ssla.html")

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    
    