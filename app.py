import os
from flask import Flask, flash, render_template, redirect, request, session, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/lolas_cookbook")
def lolas_cookbook():
    return render_template("index.html")


@app.route("/get_recipes")
def get_recipes():
    recipes = list(mongo.db.recipes.find())
    return render_template("recipes.html", recipes=recipes)


@app.route("/get_mealplanner")
def get_mealplanner():
    return render_template("mealplanner.html")


@app.route("/add_recipes", methods=["GET", "POST"])
def add_recipes():
    if request.method == "POST":
        recipes = {
            "category_name": request.form.get("category_name"),
            "recipe_name": request.form.get("recipe_name"),
            "recipe_description": request.form.get("recipe_description"),
            "family_story": request.form.get("family_story"),
            "recipe_ingredients": request.form.get("recipe_ingredients"),
            "cooking_instruction": request.form.get("cooking_instruction"),
            "recipe_day": request.form.get("recipe_day")
        }
        mongo.db.recipes.insert_one(recipes)
        flash("Your recipe is succesfully added")
        return redirect(url_for("get_recipes"))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_recipes.html", categories=categories)

    mealplanner_date = mongo.db.mealplanner_date.find().sort("recipe_day", 1)
    return render_template("add_recipes.html", mealplanner_date=mealplanner_date)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)