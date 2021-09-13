import os
import sql_queries as queries
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
    sql = queries.courses_all
    result = db.session.execute(sql)
    courses = result.fetchall()
    if session.get("firstname"):
        sql_user = queries.courses_user
        result_user = db.session.execute(sql_user, {"user_id":session["username"]})
        courses_user = result_user.fetchall()
        return render_template("index.html",courses=courses,courses_user=courses_user)   
    return render_template("index.html",courses=courses)

@app.route("/adduser", methods=["POST"])
def adduser():
    username = request.form["username"]
    password = request.form["password"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    phone = request.form["phone"]
    bornyear = request.form["bornyear"]

    hash_value = generate_password_hash(password)

    session["firstname"] = firstname
    session["username"] = username
    session["usertype"] = 'student'
    sql = "INSERT INTO userstest VALUES" \
        "(:username, :password, :firstname, :lastname, :phone, :bornyear, :usertype, :removed)"
    db.session.execute(sql, {"username":username, "password":hash_value,"firstname":firstname, "lastname":lastname,
     "phone":phone, "bornyear":bornyear, "usertype":"student", "removed":False})
    db.session.commit()
    return redirect("/") 


@app.route("/error")
def error():
    return render_template("error.html")    

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT username, password, firstname, usertype FROM userstest WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if not user:
        return redirect("/error") 
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):#the latter is the plaintext version
            session["firstname"] = user.firstname # here we set the session info
            session["username"] = user.username # here we set the session info
            session["usertype"] = user.usertype # here we set the session info
            return redirect("/")
        else:
            return redirect("/error")   

@app.route("/logout", methods=["POST"])
def logout():
    del session["firstname"] # here we remove the session info
    del session["username"]
    del session["usertype"]
    return redirect("/")

@app.route("/register", methods=["POST"])
def register():
    return render_template("register.html")

@app.route("/rooms")
def rooms():
    sql = queries.rooms
    result = db.session.execute(sql)
    rooms = result.fetchall()
    print(rooms)
    return render_template("rooms.html",rooms=rooms)

