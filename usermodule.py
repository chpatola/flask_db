"""User related functions called by routes.py"""
import secrets
from flask import session
from werkzeug.security import generate_password_hash
import sql_queries as queries
from db import db

def add_user(username, firstname, lastname, phone, bornyear, hash_value):
    session["firstname"] = firstname
    session["username"] = username
    session["usertype"] = 'student'
    session["csrf_token"] = secrets.token_hex(16)
    db.session.execute(queries.add_user, {"username": username, "password": hash_value, "firstname": firstname,
                                          "lastname": lastname, "phone": phone, "bornyear": bornyear, "usertype": "student",
                                          "removed": False})
    db.session.commit()

def check_duplicate_users(username):
    duplicant_user=db.session.execute(queries.userdata, {"username": username}).fetchone()
    return duplicant_user

def edit_user(firstname, lastname, phone, bornyear):
    db.session.execute(queries.edit_user, {"username": session["username"], "firstname": firstname,
                                           "lastname": lastname, "phone": phone, "bornyear": bornyear})
    db.session.commit()


def edit_user_and_password(hash_value, firstname, lastname, phone, bornyear):
    db.session.execute(queries.edit_user_new_psw,
                       {"username": session["username"], "firstname": firstname, "lastname": lastname,
                        "phone": phone, "bornyear": bornyear, "newpassword": hash_value})
    db.session.commit()

def get_new_user_data(request):
    username = request.form["username"].lower()
    password = request.form["password"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    phone = request.form["phone"]
    bornyear = request.form["bornyear"]
    hash_value = generate_password_hash(password)
    return username, firstname, lastname, phone, bornyear, hash_value

def find_user(request):
    user = db.session.execute(queries.find_user, {"username": session["username"]}).fetchone()
    password = request.form["password"]
    newpassword = request.form["newpassword"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    phone = request.form["phone"]
    bornyear = request.form["bornyear"]
    return user, password, newpassword, firstname, lastname, phone, bornyear

def users_courses():
    result = db.session.execute(
        queries.check_users_courses,
        {"username": session["username"]}).fetchone()
    return result

def remove_user():
    db.session.execute(queries.remove_user,
                       {"username": session["username"]})
    db.session.commit()
