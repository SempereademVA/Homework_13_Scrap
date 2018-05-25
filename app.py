# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import time

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app)


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars_data = mongo.db.collection.find()


    print()
    print("************ HOME **********")
    print('Found Data')
    print()


    # return template and data
    return render_template("index.html", mars=mars_data)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Run scraped functions
    mars1 = scrape_mars.scrape_mars()
    print()
    print('Scraping done!')

    print('Add to Database')
    print("==> back at the /scrape route")
    mongo.db.collection.drop()
    mongo.db.collection.insert_one(mars1)
   
    return redirect("http://localhost:5000/", code=302)
    # Redirect back to home page

        # Insert Mars Data into database



if __name__ == "__main__":
    app.run(debug=True)
