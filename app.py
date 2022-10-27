from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# set up Flask
app = Flask(__name__)

# need to tell Python how to connect to Mongo using PyMongo

# Use flask_pymongo to set up mongo connection
# tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL.
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app" # <--is the URI we'll be using to connect our app to Mongo
app.config["TEMPLATES_AUTO_RELOAD"] = True

mongo = PyMongo(app)

#define route for html page
@app.route("/")
def index():

    mars = mongo.db.mars.find_one()

    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():

    mars = mongo.db.mars

    mars_data = scraping.scrape_all()

    mars.update_one({}, {"$set":mars_data}, upsert=True)

    return redirect('/', code=302)

if __name__=="__main__":

    app.run()