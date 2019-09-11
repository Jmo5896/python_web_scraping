from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
from login_db import myKeys
keys = myKeys()
app = Flask(__name__)

app.config["MONGO_URI"] = f"mongodb://{keys['userName']}:{keys['password']}@ds011268.mlab.com:11268/heroku_p589mnvp"

# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route('/')
def home():
    mars_data = mongo.db.mars_data.find_one()
    # print(mars_data)
    return render_template('index.html', mars_data = mars_data)

@app.route('/scrape')
def scrape():
    mars_data = scrape_mars.scrape_mars()
    mongo.db.mars_data.update({},mars_data, upsert=True)
    # print(mars_data)
    return redirect('/')

if __name__ == "__main__":
    app.run()