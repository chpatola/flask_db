"""General functions called by routes.py"""
from flask import session, request
import error_texts as errortext
import sql_queries as queries
from db import db

def logout():
    del session["firstname"] 
    del session["username"]
    del session["usertype"]
    del session["csrf_token"]

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