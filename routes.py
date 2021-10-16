"""Routes and their functionalities"""
#import os
from datetime import date
import secrets
from os import abort, getenv
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import sql_queries as queries
import error_texts as errortext
import general
import course
import teacher
import user
from app import app
from db import db


@app.route("/")
def index():
    courses_upcoming = general.show_upcoming_courses()
    if session.get("firstname"):
        users_courses = general.show_users_courses()
        courses_ongoing = general.show_ongoing_courses()
        return render_template("index.html", 
                               courses_ongoing=courses_ongoing, courses_upcoming=courses_upcoming,
                               users_courses=users_courses, today=date.today())
    return render_template("index.html", courses_upcoming=courses_upcoming)

@app.route("/addcourse", methods=["POST"])
def addcourse():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    name,startdate,enddate,time,duration,occurances,price,teacher,room = course.get_new_course_data(request)
    if startdate > enddate:
        return render_template("error.html", errortext=errortext.incorrect_timespan)      
    if session["usertype"] == 'admin':
        try:
            course.add_course(name,startdate,enddate,time,duration,occurances,price,teacher,room)
            return redirect("/")
        except:
            return render_template("error.html", errortext=errortext.incorrect_input)    
    return render_template("error.html", errortext=errortext.access_missing)     

@app.route("/addteacher", methods=["POST"])
def addteacher():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    firstname,lastname,phone,email,hourlysalary = teacher.get_new_teacher_data(request)
    if session["usertype"] == 'admin':
        try:
            teacher.add_teacher(firstname,lastname,phone,email,hourlysalary)
            return redirect("/teachers")
        except:
            return render_template("error.html", errortext=errortext.incorrect_input)
    return render_template("error.html", errortext=errortext.access_missing) 

@app.route("/adduser", methods=["POST"])
def adduser():
    username = request.form["username"].lower()
    password = request.form["password"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    phone = request.form["phone"]
    bornyear = request.form["bornyear"]
    hash_value = generate_password_hash(password)
    try:
        session["firstname"] = firstname
        session["username"] = username
        session["usertype"] = 'student'
        session["csrf_token"] = secrets.token_hex(16)
        db.session.execute(queries.add_user, {"username": username, "password": hash_value, "firstname": firstname,
                                              "lastname": lastname,"phone": phone, "bornyear": bornyear, "usertype": "student",
                                              "removed": False})
        db.session.commit()
        return redirect("/")
    except:
        return render_template("error", errortext=errortext.incorrect_input)

@app.route("/disenrolcourse/<int:id>")
def disenrolcourse(id):
    if session["username"]:  
        course.disenrol_course(id) 
        return redirect("/")
    return render_template("error.html", errortext=errortext.access_missing)    

@app.route("/edituser", methods=["POST"])
def edituser():
    if session["username"]:
        user = db.session.execute(queries.find_user, {"username": session["username"]}).fetchone()
        password = request.form["password"]
        newpassword = request.form["newpassword"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        phone = request.form["phone"]
        bornyear = request.form["bornyear"]
        if check_password_hash(user.password, password):
            if len(newpassword) > 3:
                try:
                    hash_value = generate_password_hash(newpassword)
                    db.session.execute(queries.edit_user_new_psw,
                                       {"username": session["username"], "firstname": firstname, "lastname": lastname,
                                        "phone": phone, "bornyear": bornyear, "newpassword": hash_value})
                    db.session.commit()
                    return redirect("/userprofile")
                except:
                    return render_template("error.html", errortext=errortext.incorrect_input)    
            else:
                try:
                    db.session.execute(queries.edit_user, {"username": session["username"], "firstname": firstname,
                                                           "lastname": lastname, "phone": phone, "bornyear": bornyear})
                    db.session.commit()
                    return redirect("/userprofile")
                except:
                    return render_template("error.html", errortext=errortext.incorrect_input)     
        else:
            return render_template("error.html", errortext=errortext.login_error) 
    return render_template("error.html", errortext=errortext.access_missing)

@app.route("/enrolcourse/<int:id>")
def enrolcourse(id):
    registrated = db.session.execute(
        queries.check_users_course, {"username": session["username"], "id": id}).fetchone()
    if registrated[0] > 0:
        return render_template("error.html", errortext=errortext.already_registered)
    course.enrol_course(id)
    return redirect("/")

@app.route("/enrolledstudents/<int:id>")
def enrolledstudents(id):
    if session["usertype"] == 'admin':
        enrolled_users = db.session.execute(queries.users_course, {"id": id}).fetchall()
        return render_template("enrolledstudents.html", enrolled_users=enrolled_users, id=id)
    return redirect("/")    

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"].lower()
    password = request.form["password"]

    user = db.session.execute(queries.find_user, {"username": username}).fetchone()
    if not user:
        return render_template("error.html", errortext=errortext.login_error) 
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["firstname"] = user.firstname
            session["username"] = user.username 
            session["usertype"] = user.usertype  
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        return render_template("error.html", errortext=errortext.login_error)

@app.route("/logout", methods=["POST", "GET"])
def logout():
    general.logout()    
    return redirect("/")

@app.route("/registercourse", methods=["POST"])
def registercourse():
    if session["usertype"] == 'admin':
        teachers = db.session.execute(queries.teachers).fetchall()
        rooms = db.session.execute(queries.rooms).fetchall()
        return render_template("registercourse.html", rooms=rooms, teachers=teachers)
    return render_template("error.html", errortext=errortext.access_missing)  

@app.route("/registerteacher", methods=["POST"])
def registerteacher():
    if session["usertype"] == 'admin':
        return render_template("registerteacher.html")
    return render_template("error.html", errortext=errortext.access_missing)    

@app.route("/registeruser", methods=["POST"])
def registeruser():
    return render_template("registeruser.html")

@app.route("/removecourse/<int:id>")
def removecourse(id):
    if session["usertype"] == 'admin':
        enrolled_users = db.session.execute(queries.users_course, {"id": id}).fetchall()
        if len(enrolled_users) > 0:
            return render_template("error.html", errortext=errortext.course_has_students)  
        course.remove_course()
        return redirect("/")
    return render_template("error.html", errortext=errortext.access_missing)  

@app.route("/removeuser")
def removeuser():
    if session["username"]:
        users_courses = user.users_courses()
        if users_courses[0] > 0:
            return render_template("error.html", errortext=errortext.account_remove_error)  
        user.remove_user()
        return redirect("/logout")
    return render_template("error.html", errortext=errortext.access_missing)  

@app.route("/rooms")
def rooms():
    if session["usertype"] == 'admin':
        rooms = db.session.execute(queries.rooms).fetchall()
        return render_template("rooms.html", rooms=rooms)
    return render_template("error.html", errortext=errortext.access_missing)  

@app.route("/teachers")
def teachers():
    if session["usertype"] == 'admin':
        teachers = db.session.execute(queries.teachers).fetchall()
        return render_template("teachers.html", teachers=teachers)
    return render_template("error.html", errortext=errortext.access_missing)  

@app.route("/userprofile")
def userprofile():
    if session["username"]:
        userdata = db.session.execute(queries.userdata, {"username": session["username"]}).fetchone()
        return render_template("userprofile.html", userdata=userdata)
    return render_template("error.html", errortext=errortext.access_missing)
