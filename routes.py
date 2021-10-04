import os
import sql_queries as queries
import error_texts as errortext
import secrets
from app import app
from db import db
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import abort, getenv
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date


@app.route("/")
def index():
    courses_upcoming = db.session.execute(queries.courses_upcoming).fetchall()

    if session.get("firstname"):

        courses_user = db.session.execute(
            queries.courses_user, {"user_id": session["username"]}).fetchall()
        courses_ongoing = db.session.execute(queries.courses_ongoing).fetchall()
        return render_template("index.html", courses_ongoing=courses_ongoing, courses_upcoming=courses_upcoming, courses_user=courses_user, today=date.today())
    return render_template("index.html", courses_upcoming=courses_upcoming)


@app.route("/addcourse", methods=["POST"])
def addcourse():
    if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
    name = request.form["name"]
    startdate = request.form["startdate"]
    enddate = request.form["enddate"]
    time = request.form["time"]
    duration = request.form["duration"]
    occurances = request.form["occurances"]
    price = request.form["price"]
    teacher = request.form["teacher"]
    room = request.form["room"]

    if session["usertype"] == 'admin':
        try:
            db.session.execute(queries.add_course, {
                "name": name, "startdate": startdate, "enddate": enddate, "time": time, "duration": duration, "occurances": occurances, "price": price, "teacher_id": teacher, "room_id": room})
            db.session.commit()
            return redirect("/")
        except:
            return render_template("error.html", errortext=errortext.incorrect_input)    
    else: 
        return render_template("error.html",errortext=errortext.access_missing)     


@app.route("/addteacher", methods=["POST"])
def addteacher():
    if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    phone = request.form["phone"]
    email = request.form["email"]
    hourlysalary = request.form["hourlysalary"]
    if session["usertype"] == 'admin':
        try:
            db.session.execute(queries.add_teacher, {"firstname": firstname, "lastname": lastname,
                                    "phone": phone, "email": email, "hourlysalary": hourlysalary})
            db.session.commit()
            return redirect("/teachers")
        except:
            return render_template("error.html",errortext=errortext.incorrect_input)

    else:
        return render_template("error.html",errortext=errortext.access_missing) 

@app.route("/adduser", methods=["POST"])
def adduser():
    username = request.form["username"]
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
        print(session["csrf_token"])
        db.session.execute(queries.add_user, {"username": username, "password": hash_value, "firstname": firstname, "lastname": lastname,
                                "phone": phone, "bornyear": bornyear, "usertype": "student", "removed": False})
        db.session.commit()
        return redirect("/")
    except:
        return render_template("error",errortext=errortext.incorrect_input)

@app.route("/disenrolcourse/<int:id>")
def disenrolcourse(id):
    if session["username"]:
        db.session.execute(queries.disenrol_course, {"username": session["username"], "id": id})
        db.session.commit()
        return redirect("/")
    else:
        return render_template("error.html",errortext=errortext.access_missing)    


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
                    db.session.execute(queries.edit_userpsw,
                                    {"username": session["username"], "firstname": firstname, "lastname": lastname, "phone": phone, "bornyear": bornyear, "newpassword": hash_value})
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
            return render_template("error.html",errortext=errortext.login_error) 
    else:
        return render_template("error.html",errortext=errortext.access_missing)


@app.route("/enrolcourse/<int:id>")
def enrolcourse(id):
    registrated = db.session.execute(
        queries.check_users_course, {"username": session["username"], "id": id}).fetchone()
    if registrated[0] > 0:
        return render_template("error.html",errortext=errortext.already_registered)
    else:
        db.session.execute(queries.enrol_course, {"username": session["username"], "id": id})
        db.session.commit()
        return redirect("/")

@app.route("/enrolledstudents/<int:id>")
def enrolledstudents(id):
    if session["usertype"] == 'admin':
        enrolled_users = db.session.execute(queries.users_course, {"id": id}).fetchall()
        return render_template("enrolledstudents.html", enrolled_users=enrolled_users, id=id)
    else:
        return redirect("/")    

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = db.session.execute(queries.find_user, {"username": username}).fetchone()
    if not user:
        return render_template("error.html",errortext=errortext.login_error) 
    else:
        hash_value = user.password
        # the latter is the plaintext version
        if check_password_hash(hash_value, password):
            # here we set the session info
            session["firstname"] = user.firstname
            session["username"] = user.username  # here we set the session info
            session["usertype"] = user.usertype  # here we set the session info
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            return render_template("error.html",errortext=errortext.login_error)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    del session["firstname"]  # here we remove the session info
    del session["username"]
    del session["usertype"]
    del session["csrf_token"]
    return redirect("/")


@app.route("/registercourse",methods=["POST"])
def registercourse():
    if session["usertype"] == 'admin':
        teachers = db.session.execute(queries.teachers).fetchall()
        rooms = db.session.execute(queries.rooms).fetchall()
        return render_template("registercourse.html", rooms=rooms, teachers=teachers)
    else:
        return render_template("error.html",errortext=errortext.access_missing)  

@app.route("/registerteacher",methods=["POST"])
def registerteacher():
    if session["usertype"] == 'admin':
        return render_template("registerteacher.html")
    else:
        return render_template("error.html",errortext=errortext.access_missing)    


@app.route("/registeruser", methods=["POST"])
def registeruser():
    return render_template("registeruser.html")


@app.route("/removecourse/<int:id>")
def removecourse(id):
    if session["usertype"] == 'admin':
        enrolled_users = db.session.execute(queries.users_course, {"id": id}).fetchall()
        if len(enrolled_users) > 0:
            return render_template("error.html",errortext=errortext.course_has_students)  
        else:
            db.session.execute(queries.remove_course, {"id": id})
            db.session.commit()
            return redirect("/")
    else:
        return render_template("error.html",errortext=errortext.access_missing)  


@app.route("/removeuser")
def removeuser():
    if session["username"]:
        users_courses = db.session.execute(
            queries.check_users_courses, {"username": session["username"]}).fetchone()
        if users_courses[0] > 0:
            return render_template("error.html",errortext=errortext.account_remove_error)  
        else:
            db.session.execute(queries.remove_user, {"username": session["username"]})
            db.session.commit()
            return redirect("/logout")
    else:
        return render_template("error.html",errortext=errortext.access_missing)  

@app.route("/rooms")
def rooms():
    if session["usertype"] == 'admin':
        rooms = db.session.execute(queries.rooms).fetchall()
        return render_template("rooms.html", rooms=rooms)
    else:
        return render_template("error.html",errortext=errortext.access_missing)  

@app.route("/teachers")
def teachers():
    if session["usertype"] == 'admin':
        teachers = db.session.execute(queries.teachers).fetchall()
        return render_template("teachers.html", teachers=teachers)
    else:
        return render_template("error.html",errortext=errortext.access_missing)  

@app.route("/userprofile")
def userprofile():
    if session["username"]:
        userdata = db.session.execute(queries.userdata, {"username": session["username"]}).fetchone()
        return render_template("userprofile.html", userdata=userdata)
    else:
        return render_template("error.html",errortext=errortext.access_missing)
