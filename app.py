import os
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #Supress warning
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/error")
def error():
    return render_template("error.html")    

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT username, password FROM userstest WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if not user:
        return redirect("/error") 
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):#the latter is the plaintext version
            session["username"] = username
            return redirect("/")
        else:
            return redirect("/error")   

if __name__=="__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 4444)))