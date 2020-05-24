from flask import Flask, render_template, redirect,jsonify
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017")

@app.route("/")
def home():

    mars = mongo.db.collection.find_one()
    return render_template("index.html",)


@app.route("/scrape")
def scrape():



if __name__ == "__main__":
    app.run(debug=True)