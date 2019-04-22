import os
import requests
from models import *
from flask import Flask, session,render_template, request, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['DEBUG'] = 1
db.init_app(app)


# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("home.html")

# @app.route("/test", methods = ["POST", "GET"])
# def test():
#     if request.method == "POST":
#         r = Recipe.query.first()
#         return jsonify({"success": True, "name":r.name, "ing":r.ingredients, "steps":r.steps})
#     else:
#         r = Recipe.query.first()
#         return r.ingredients

@app.route("/recipes")
def recipes():
    return render_template("recipes.html")

@app.route("/recipes/<string:id>")
def recipe(id):
    try:
        id = int(id)
    except ValueError:
        return ("Get the hell out of here")
    r = Recipe.query.filter_by(id = id).first()
    if r != None:
        return render_template('recipe_template.html', this_recipe = r, this_steps = step_handler(r.ingredients))
    else:
        return ("Error: Invalid recipe")
