import os
import requests
import random
from models import *
from flask import Flask, session, render_template, request, redirect, jsonify
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


@app.route("/")
def index():
    r = Recipe.query.all()
    return render_template("home.html", recipes_list=r)


@app.route("/recipes")
def recipes():
    # r = Recipe.query.all()
    # return render_template("recipes.html", recipes_list = r)
    l = random.sample(Recipe.query.all(), 3)
    return render_template('recipes.html', random_recipes=l)


@app.route("/recipes/<string:id>")
def recipe(id):
    try:
        id = int(id)
    except ValueError:
        return ("Get the hell out of here")
    r = Recipe.query.filter_by(id=id).first()
    l = random.sample(Recipe.query.all(), 3)
    a = Recipe.query.all()
    if r != None:
        return render_template('recipe_template.html', this_recipe=r, this_ingredients=ingredient_handler(r.ingredients), this_steps=step_handler(r.steps), random_recipes=l, recipes_list=a)
    else:
        return ("Error: Invalid recipe")


@app.route("/random")
def random_recipe():
    r = random.choice(Recipe.query.all())
    return redirect("/recipes/" + str(r.id))


@app.route("/search", methods=["POST"])
def search_recipe():
    recipe_name = request.form.get('name')
    r = Recipe.query.filter_by(name=recipe_name).first()
    if r != None:
        return redirect("/recipes/"+str(r.id))
    else:
        return ("Error: Invalid recipe")


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    ingredients = request.form.get('ingredients')
    steps = request.form.get('steps')
    yields = request.form.get('yields')
    url = request.form.get('url')
    this_recipe = Recipe(name=name, ingredients=ingredients,
                         steps=steps, yields=yields, url=url)
    db.session.add(this_recipe)
    db.session.commit()
    return redirect("/recipes/"+str(this_recipe.id))


if __name__ == "__main__":
    app.run()
