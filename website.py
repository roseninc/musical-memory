from flask import Flask, render_template
from flask import request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:vc68HvL7Py5PdgK4@34.89.101.80/teaminternational'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\danie\Desktop\WebsiteLATEST\data.db'
db = SQLAlchemy(app)


class climate(db.Model):
    reading_time = db.Column('reading_time', db.DateTime, primary_key=True)
    temp = db.Column(db.Float)
    hum = db.Column(db.Float)
    gpslat = db.Column(db.Float)
    gpslong = db.Column(db.Float)
    light = db.Column(db.Float)

    def __init__(self, temp, hum, gpslat, gpslong, light):
        self.temp = temp
        self.hum = hum
        self.gpslat = gpslat
        self.gpslong = gpslong
        self.light = light

class login(db.Model):
    user_name = db.Column(db.Text, primary_key = True)
    password = db.Column(db.Integer)

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password

@app.route('/')
def login_page():
    login_data = login.query.all()
    return render_template("login_page.html", login_data = login_data)


@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/data")
def data():
    live_data = climate.query.all()
    return render_template("data.html", live_data = live_data)


@app.route("/database")
def database():
    myClimate = climate.query.all()
    return render_template('database.html', myClimate=myClimate)


@app.route("/map")
def map():
    gps_data = climate.query.all()
    return render_template("map.html", gps_data = gps_data)


@app.route("/graphs")
def graphs():
    return render_template("graphs.html")


if __name__ == "__main__":
    app.run(debug=True)
