"""User related functions called by routes.py"""
from flask import session, request
import error_texts as errortext
import sql_queries as queries
from db import db

def users_courses():
    result = db.session.execute(
            queries.check_users_courses, 
             {"username": session["username"]}).fetchone()
    return(result)

def remove_user():
    db.session.execute(queries.remove_user, 
     {"username": session["username"]})
    db.session.commit()
