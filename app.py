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

@app.route("/addteacher",methods=["POST"])
def addteacher():
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    phone = request.form["phone"]
    email = request.form["email"]
    hourlysalary = request.form["hourlysalary"]
    sql = queries.add_teacher
    db.session.execute(sql, {"firstname":firstname, "lastname":lastname,
     "phone":phone, "email":email, "hourlysalary":hourlysalary})
    db.session.commit()
    return redirect("/teachers") 

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
    sql = queries.add_user
    db.session.execute(sql, {"username":username, "password":hash_value,"firstname":firstname, "lastname":lastname,
     "phone":phone, "bornyear":bornyear, "usertype":"student", "removed":False})
    db.session.commit()
    return redirect("/") 

@app.route("/enrolcourse/<int:id>")
def enrolcourse(id):
    sql = queries.check_users_course
    result = db.session.execute(sql, {"username":session["username"],"id":id})
    registrated = result.fetchone()
    if registrated[0] >0:
        return redirect("/error")
    else:
        sql = queries.enrol_course
        db.session.execute(sql, {"username":session["username"],"id":id})
        db.session.commit()
        return redirect("/")

   
@app.route("/error")
def error():
    return render_template("error.html")    

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = queries.find_user
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

@app.route("/logout",methods=["POST","GET"])
def logout():
    del session["firstname"] # here we remove the session info
    del session["username"]
    del session["usertype"]
    return redirect("/")

@app.route("/registerteacher")
def registerteacher():
    return render_template("registerteacher.html")

@app.route("/registeruser", methods=["POST"])
def registeruser():
    return render_template("registeruser.html")

@app.route("/removeuser")
def removeuser():
    sql_users_courses = queries.check_users_courses
    result_users_course = db.session.execute(sql_users_courses,{"username":session["username"]})
    users_courses = result_users_course.fetchone()
    if users_courses[0]  > 0:
        return render_template("error")
    else: 
        sql_remove = queries.remove_user
        db.session.execute(sql_remove,{"username":session["username"]})
        db.session.commit()
        return redirect("/logout")

@app.route("/rooms")
def rooms():
    sql = queries.rooms
    result = db.session.execute(sql)
    rooms = result.fetchall()
    return render_template("rooms.html",rooms=rooms)

@app.route("/teachers")
def teachers():
    sql = queries.teachers
    result = db.session.execute(sql)
    teachers = result.fetchall()
    return render_template("teachers.html",teachers=teachers)

@app.route("/userprofile")
def userprofile():
    return render_template("userprofile.html")