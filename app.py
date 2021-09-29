import os
import sql_queries as queries
import error_texts as errortext
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Supress warning
db = SQLAlchemy(app)


@app.route("/")
def index():
    sql_upcoming = queries.courses_upcoming
    result_upcoming = db.session.execute(sql_upcoming)
    courses_upcoming = result_upcoming.fetchall()

    if session.get("firstname"):
        sql_user = queries.courses_user
        result_user = db.session.execute(
            sql_user, {"user_id": session["username"]})
        courses_user = result_user.fetchall()

        sql_ongoing = queries.courses_ongoing
        result_ongoing = db.session.execute(sql_ongoing)
        courses_ongoing = result_ongoing.fetchall()
        return render_template("index.html", courses_ongoing=courses_ongoing, courses_upcoming=courses_upcoming, courses_user=courses_user, today=date.today())
    return render_template("index.html", courses_upcoming=courses_upcoming)


@app.route("/addcourse", methods=["POST"])
def addcourse():
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
            sql = queries.add_course
            db.session.execute(sql, {
                "name": name, "startdate": startdate, "enddate": enddate, "time": time, "duration": duration, "occurances": occurances, "price": price, "teacher_id": teacher, "room_id": room})
            db.session.commit()
            return redirect("/")
        except:
            return render_template("error.html", errortext=errortext.incorrect_input)    
    else: 
        return render_template("error.html",errortext=errortext.access_missing)     


@app.route("/addteacher", methods=["POST"])
def addteacher():
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    phone = request.form["phone"]
    email = request.form["email"]
    hourlysalary = request.form["hourlysalary"]
    if session["usertype"] == 'admin':
        try:
            sql = queries.add_teacher
            db.session.execute(sql, {"firstname": firstname, "lastname": lastname,
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
        sql = queries.add_user
        db.session.execute(sql, {"username": username, "password": hash_value, "firstname": firstname, "lastname": lastname,
                                "phone": phone, "bornyear": bornyear, "usertype": "student", "removed": False})
        db.session.commit()
        return redirect("/")
    except:
        return render_template("error",errortext=errortext.incorrect_input)

@app.route("/disenrolcourse/<int:id>")
def disenrolcourse(id):
    if session["username"]:
        sql = queries.disenrol_course
        db.session.execute(sql, {"username": session["username"], "id": id})
        db.session.commit()
        return redirect("/")
    else:
        return render_template("error.html",errortext=errortext.access_missing)    


@app.route("/edituser", methods=["POST"])
def edituser():
    if session["username"]:
        sql = queries.find_user
        result = db.session.execute(sql, {"username": session["username"]})
        user = result.fetchone()

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
                    sql = queries.edit_userpsw
                    db.session.execute(sql,
                                    {"username": session["username"], "firstname": firstname, "lastname": lastname, "phone": phone, "bornyear": bornyear, "newpassword": hash_value})
                    db.session.commit()
                    return redirect("/userprofile")
                except:
                    return render_template("error.html", errortext=errortext.incorrect_input)    
            else:
                try:
                    sql = queries.edit_user
                    print(sql)
                    db.session.execute(sql, {"username": session["username"], "firstname": firstname,
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
    sql = queries.check_users_course
    result = db.session.execute(
        sql, {"username": session["username"], "id": id})
    registrated = result.fetchone()
    if registrated[0] > 0:
        return render_template("error.html",errortext=errortext.already_registered)
    else:
        sql = queries.enrol_course
        db.session.execute(sql, {"username": session["username"], "id": id})
        db.session.commit()
        return redirect("/")


@app.route("/enrolledstudents/<int:id>")
def enrolledstudents(id):
    if session["usertype"] == 'admin':
        sql = queries.users_course
        result = db.session.execute(sql, {"id": id})
        enrolled_users = result.fetchall()
        return render_template("enrolledstudents.html", enrolled_users=enrolled_users, id=id)
    else:
        return redirect("/")    


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = queries.find_user
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
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
            return redirect("/")
        else:
            return render_template("error.html",errortext=errortext.login_error)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    del session["firstname"]  # here we remove the session info
    del session["username"]
    del session["usertype"]
    return redirect("/")


@app.route("/registercourse",methods=["POST"])
def registercourse():
    if session["usertype"] == 'admin':
        sql_teachers = queries.teachers
        result_teachers = db.session.execute(sql_teachers)
        teachers = result_teachers.fetchall()

        sql_rooms = queries.rooms
        result_rooms = db.session.execute(sql_rooms)
        rooms = result_rooms.fetchall()
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
        sql = queries.users_course
        result = db.session.execute(sql, {"id": id})
        enrolled_users = result.fetchall()
        if len(enrolled_users) > 0:
            return render_template("error.html",errortext=errortext.course_has_students)  
        else:
            sql = queries.remove_course
            db.session.execute(sql, {"id": id})
            db.session.commit()
            return redirect("/")
    else:
        return render_template("error.html",errortext=errortext.access_missing)  



@app.route("/removeuser")
def removeuser():
    if session["username"]:
        sql_users_courses = queries.check_users_courses
        result_users_course = db.session.execute(
            sql_users_courses, {"username": session["username"]})
        users_courses = result_users_course.fetchone()
        if users_courses[0] > 0:
            return render_template("error.html",errortext=errortext.account_remove_error)  
        else:
            sql_remove = queries.remove_user
            db.session.execute(sql_remove, {"username": session["username"]})
            db.session.commit()
            return redirect("/logout")
    else:
        return render_template("error.html",errortext=errortext.access_missing)  

@app.route("/rooms")
def rooms():
    if session["usertype"] == 'admin':
        sql = queries.rooms
        result = db.session.execute(sql)
        rooms = result.fetchall()
        return render_template("rooms.html", rooms=rooms)
    else:
        return render_template("error.html",errortext=errortext.access_missing)  

@app.route("/teachers")
def teachers():
    if session["usertype"] == 'admin':
        sql = queries.teachers
        result = db.session.execute(sql)
        teachers = result.fetchall()
        return render_template("teachers.html", teachers=teachers)
    else:
        return render_template("error.html",errortext=errortext.access_missing)  

@app.route("/userprofile")
def userprofile():
    if session["username"]:
        sql = queries.userdata
        result = db.session.execute(sql, {"username": session["username"]})
        userdata = result.fetchone()
        return render_template("userprofile.html", userdata=userdata)
    else:
        return render_template("error.html",errortext=errortext.access_missing)
