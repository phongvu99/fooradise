from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    __tablename__ = "recipes"
    name = db.Column(db.String, nullable = False)
    ingredients = db.Column(db.String, nullable = False)
    steps = db.Column(db.String, nullable = False)
    yields = db.Column(db.String, nullable = False)
    url = db.Column(db.String, nullable = False)
    id = db.Column(db.Integer, primary_key=True)

def step_handler(steps):
    steps = steps.split("-")
    return steps
