"""Course related functions called by routes.py"""
from flask import session
import sql_queries as queries
from db import db

def get_new_course_data(request):
    name = request.form["name"]
    startdate = request.form["startdate"]
    enddate = request.form["enddate"]
    time = request.form["time"]
    duration = request.form["duration"]
    occurances = request.form["occurances"]
    price = request.form["price"]
    teacher = request.form["teacher"]
    room = request.form["room"]
    return name, startdate, enddate, time, duration, occurances, price, teacher, room

def add_course(name, startdate, enddate, time, duration, occurances, price, teacher, room):
    db.session.execute(queries.add_course, {
                "name": name, "startdate": startdate, "enddate": enddate, "time": time,
                "duration": duration, "occurances": occurances, "price": price, "teacher_id": teacher, "room_id": room})
    db.session.commit()

def disenrol_course(id):
    db.session.execute(
        queries.disenrol_course, {
            "username": session["username"], "id": id})
    db.session.commit()

def enrol_course(id):
    db.session.execute(queries.enrol_course, {"username": session["username"], "id": id})
    db.session.commit()

def remove_course(id):
    db.session.execute(queries.remove_course, {"id": id})
    db.session.commit()

def show_ongoing_courses():
    courses_ongoing = db.session.execute(
        queries.courses_ongoing).fetchall()
    return courses_ongoing

def show_users_courses():
    courses_user = db.session.execute(
        queries.courses_user, {"user_id": session["username"]}).fetchall()
    return courses_user

def show_upcoming_courses():
    courses_upcoming = db.session.execute(
        queries.courses_upcoming).fetchall()
    return courses_upcoming
