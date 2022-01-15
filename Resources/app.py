from flask import Flask, Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrapcode

app= Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config['MONGO_URI']= "mongodb://localhost:27017/mars_app"
mongo=PyMongo(app)

# Set Up Routes
@app.route("/")
def index():
    mars=mongo.db.mars.find_one()
    return render_template('TheIndex', mars=mars)

@app.route("/scrapcode")
def scrape():
   mars = mongo.db.mars
   mars_data = scrapcode.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)
   

if __name__ == "__main__":
    app.run(debug=True)
