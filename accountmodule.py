"""General functions called by routes.py"""
import secrets
from flask import session
import sql_queries as queries
from db import db

def login_attempt(request):
    username = request.form["username"].lower().strip()
    password = request.form["password"]
    user = db.session.execute(queries.find_user, {"username": username}).fetchone()
    return user, password

def login_success(user):
    session["firstname"] = user.firstname
    session["username"] = user.username
    session["usertype"] = user.usertype
    session["csrf_token"] = secrets.token_hex(16)

def logout():
    del session["firstname"]
    del session["username"]
    del session["usertype"]
    del session["csrf_token"]
