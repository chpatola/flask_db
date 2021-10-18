"""Routes and their functionalities"""
#import os
from datetime import date
from os import abort
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import exc
import sql_queries as queries
import error_texts as errortext
import accountmodule
import coursemodule
import teachermodule
import usermodule
from app import app
from db import db


@app.route("/")
def index():
    courses_upcoming = coursemodule.show_upcoming_courses()
    if session.get("firstname"):
        users_courses = coursemodule.show_users_courses()
        courses_ongoing = coursemodule.show_ongoing_courses()
        return render_template("index.html", 
                               courses_ongoing=courses_ongoing, courses_upcoming=courses_upcoming,
                               users_courses=users_courses, today=date.today())
    return render_template("index.html", courses_upcoming=courses_upcoming)

@app.route("/addcourse", methods=["POST"])
def addcourse():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    name, startdate, enddate, time, duration, occurances, price, teacher, room = coursemodule.get_new_course_data(request)
    if startdate > enddate:
        return render_template("error.html", errortext=errortext.incorrect_timespan)
    if session["usertype"] == 'admin':
        try:
            coursemodule.add_course(name, startdate, enddate, time, duration, occurances, price, teacher, room)
            return redirect("/")
        except ValueError:
            return render_template("error.html", errortext=errortext.incorrect_input) 
    return render_template("error.html", errortext=errortext.access_missing)

@app.route("/addteacher", methods=["POST"])
def addteacher():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    firstname, lastname, phone, email, hourlysalary = teachermodule.get_new_teacher_data(request)
    if session["usertype"] == 'admin':
        try:
            teachermodule.add_teacher(firstname, lastname, phone, email, hourlysalary)
            return redirect("/teachers")
        except ValueError:
            return render_template("error.html", errortext=errortext.incorrect_input)
    return render_template("error.html", errortext=errortext.access_missing)

@app.route("/adduser", methods=["POST"])
def adduser():
    username, firstname, lastname, phone, bornyear, hash_value = usermodule.get_new_user_data(request)  
    if usermodule.check_duplicate_users(username):
        return render_template("error.html", errortext=errortext.incorrect_input)
    try:
        usermodule.add_user(username, firstname, lastname, phone, bornyear, hash_value)
        return redirect("/")
    except ValueError:
            return render_template("error.html", errortext=errortext.incorrect_input)


@app.route("/disenrolcourse/<int:id>")
def disenrolcourse(id):
    if session["username"]:
        coursemodule.disenrol_course(id)
        return redirect("/")
    return render_template("error.html", errortext=errortext.access_missing)

@app.route("/edituser", methods=["POST"])
def edituser():
    if session["username"]:
        user, password, newpassword, firstname, lastname, phone, bornyear = usermodule.find_user(request)
        if check_password_hash(user.password, password):
            if len(newpassword) > 3:
                try:
                    hash_value = generate_password_hash(newpassword)
                    usermodule.edit_user_and_password(hash_value, firstname, lastname, phone, bornyear)
                    return redirect("/userprofile")
                except ValueError:
                    return render_template("error.html", errortext=errortext.incorrect_input)
            try:
                usermodule.edit_user(firstname, lastname, phone, bornyear)
                return redirect("/userprofile")
            except ValueError:
                return render_template("error.html", errortext=errortext.incorrect_input)  
        return render_template("error.html", errortext=errortext.login_error)
    return render_template("error.html", errortext=errortext.access_missing)

@app.route("/enrolcourse/<int:id>")
def enrolcourse(id):
    registrated = db.session.execute(
        queries.check_users_course, {"username": session["username"], "id": id}).fetchone()
    if registrated[0] > 0:
        return render_template("error.html", errortext=errortext.already_registered)
    coursemodule.enrol_course(id)
    return redirect("/")

@app.route("/enrolledstudents/<int:id>")
def enrolledstudents(id):
    if session["usertype"] == 'admin':
        enrolled_users = db.session.execute(queries.users_course, {"id": id}).fetchall()
        return render_template("enrolledstudents.html", enrolled_users=enrolled_users, id=id)
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    user, password = accountmodule.login_attempt(request)
    if not user:
        return render_template("error.html", errortext=errortext.login_error)
    hash_value = user.password
    if check_password_hash(hash_value, password):
        accountmodule.login_success(user)
        return redirect("/")
    return render_template("error.html", errortext=errortext.login_error)

@app.route("/logout", methods=["POST", "GET"])
def logout():
    accountmodule.logout()
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
        coursemodule.remove_course(id)
        return redirect("/")
    return render_template("error.html", errortext=errortext.access_missing)

@app.route("/removeuser")
def removeuser():
    if session["username"]:
        users_courses = usermodule.users_courses()
        if users_courses[0] > 0:
            return render_template("error.html", errortext=errortext.account_remove_error)
        usermodule.remove_user()
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
        userdata = db.session.execute(queries.userdata,
                                      {"username": session["username"]}).fetchone()
        return render_template("userprofile.html", userdata=userdata)
    return render_template("error.html", errortext=errortext.access_missing)
