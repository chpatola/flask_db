"""Database settings"""
from os import getenv
from app import app
from flask_sqlalchemy import SQLAlchemy


app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Supress warning
db = SQLAlchemy(app)
