"""Teacher functions called by routes.py"""
import sql_queries as queries
from db import db

def add_teacher(firstname, lastname, phone, email, hourlysalary):
    db.session.execute(queries.add_teacher,
                       {"firstname": firstname, "lastname": lastname,
                        "phone": phone, "email": email,
                        "hourlysalary": hourlysalary})
    db.session.commit()

def get_new_teacher_data(request):
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    phone = request.form["phone"]
    email = request.form["email"]
    hourlysalary = request.form["hourlysalary"]
    return firstname, lastname, phone, email, hourlysalary
