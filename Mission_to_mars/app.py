# create a route called /scrape to import scrape_mars.py
# call scrape function
# store returned value in mongo as py dict
# create root route / to query mongo database and pass mars data into HTML template to display data

#dependencies 
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] ="mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# create a route for homepage
@app.route("/")
def home():
    mars_info_dict = mongo.db. mars_info_dict.find_one()

    return render_template("index.html",  mars_info_dict=mars_info_dict)

# create a route for scrape
@app.route("/scrape")
def scrape():

     mars_info_dict = mongo.db.mars_info_dict
     mars_news = scrape_mars.nasa_mars()

     return redirect("/")


# app run
if __name__ == "__main__":
    app.run(debug=True)




