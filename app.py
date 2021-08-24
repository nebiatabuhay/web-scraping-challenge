from flask import Flask, render_template, jsonify, redirect
import pymongo
from flask_pymongo import PyMongo
import scrape_mars

# Instantiate a Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/marsmission_app"
mongo = PyMongo(app)

# Create a base '/' route that will query your mongodb database and render the `index.html` template
@app.route("/")
def index():
    mars = mongo.db.planet_mars.find_one()
    return render_template("index.html", planet_mars=mars)

# '/scrape' route that will create the mars collection, run scrape() function from scrape_mars, and update the mars collection in the database
# The route redirects back to the base route '/' with a code 302.
@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    mongo.db.planet_mars.update({}, mars_data, upsert = True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)