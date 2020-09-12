from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
#mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_mars_db"
#mongo=PyMongo(app)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database
    destination_data = mongo.db.marscollection.find_one()
    # Return template and data
    return render_template("index.html", mars=destination_data)
# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_news = scrape_mars.scrape_marsnews()
    mars_imageurl = scrape_mars.scrape_marsimage()
    marsfact_dict = scrape_mars.scrape_marsfacts()
    hemisphere_list = scrape_mars.scrape_marshemispheres()


    print(f"\n----------------------------")
    print(f"news  {mars_news}")
    print(f"imgage url   {mars_imageurl} ")
    print(marsfact_dict)
    print(f"hemisphere  {hemisphere_list}")
    print("-------------------------------\n")

    mars_dictionary = {'Headlines':mars_news[0], 'Details':mars_news[1], 
                    'Image':mars_imageurl,
                    'Facts':marsfact_dict,
                    'Hemisphere':hemisphere_list
                    }

    # Update the Mongo database using update and upsert=True
    mongo.db.marscollection.update({}, mars_dictionary, upsert=True)    
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
