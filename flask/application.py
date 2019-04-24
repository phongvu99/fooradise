import os
import requests
import random
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
    r = Recipe.query.all()
    return render_template("home.html", recipes_list = r)


@app.route("/recipes")
def recipes():
    return render_template("recipes.html")

@app.route("/submitRecipes")
def submitRecipes():
    return render_template("submitRecipes.html")

@app.route("/recipes/<string:id>")
def recipe(id):
    try:
        id = int(id)
    except ValueError:
        return ("Get the hell out of here")
    r = Recipe.query.filter_by(id = id).first()
    l = random.sample(Recipe.query.all(), 3)
    if r != None:
        return render_template('recipe_template.html', this_recipe = r, this_steps = step_handler(r.ingredients), random_recipes = l)
    else:
        return ("Error: Invalid recipe")

@app.route("/random")
def random_recipe():
    r = random.choice(Recipe.query.all())
    return redirect("/recipes/"+ str(r.id))

@app.route("/search", methods = ["POST"])
def search_recipe():
    recipe_name = request.form.get('name')
    r = Recipe.query.filter_by(name = recipe_name).first()
    if r != None:
        return redirect("/recipes/"+str(r.id))
    else:
        return ("Error: Invalid recipe")
