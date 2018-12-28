import pickledb
from flask_restful import Resource, Api
from flask import Flask
import string
import requests
import json
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz
import time
import atexit
import os


# Initialize Flask app and API resource
weather_service = Flask(__name__)
api = Api(weather_service)


# Function to convert unix time to human readable
def convert_time(ts):
    eastern = pytz.timezone('US/Eastern')
    time = datetime.utcfromtimestamp(ts)
    time = time.astimezone(eastern).strftime('%Y-%m-%d %I:%M %p')
    return time[12:]
    
def convert_icon(icon):
    dict = {
        "01d"	: "wi-day-sunny",
        "02d"	: "wi-day-cloudy",
        "03d"	: "wi-cloud",
        "04d"	: "wi-cloudy",
        "09d"	: "wi-rain",
        "10d"	: "wi-day-rain",
        "11d"	: "wi-day-thunderstorm",
        "13d"	: "wi-snow",
        "50d"	: "wi-fog",
        "01n"	: "wi-night-clear",
        "02n"	: "wi-night-alt-cloudy",
        "03n"	: "wi-cloud",
        "04n"	: "wi-cloudy",
        "09n"	: "wi-rain",
        "10n"	: "wi-night-rain",
        "11n"	: "wi-night-alt-thunderstorm",
        "13n"	: "wi-snow",
        "50n"	: "wi-fog"
    }

    wiicon = dict[icon]

    return wiicon

# Function to update local weather data store
def get_current():

    # Set query string values
    appid = os.environ['APIKEY']
    zip = os.environ['ZIP']
    units = "imperial"
    url = "http://api.openweathermap.org/data/2.5/weather"
    query = {"appid" : appid, "units" : units, "zip" : zip}

    # Request data from OpenWeatherMap API and store returned status code
    data = requests.request("GET", url, params=query)
    status = data.status_code
    data = data.json()

    # Check if request was successful
    if status == 200:

        # Read returned data to pick out required values
        weather = {
            "time" : datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M'),
            "temp" : round(data['main']['temp']),
            "min_temp" : round(data['main']['temp_min']),
            "max_temp" : round(data['main']['temp_max']),
            "humidity" : data['main']['humidity'],
            "icon" : convert_icon(data['weather'][0]['icon']),
            "desc" : string.capwords(data['weather'][0]['description']),
            "wind_spd" : round(data['wind']['speed']),
            "wind_dir" : round(data['wind']['deg']),
            "cloud_cvr" : 100*data['clouds']['all'],
            "sunrise" : convert_time(data['sys']['sunrise']),
            "sunset" : convert_time(data['sys']['sunset'])
        }

        # Open connection to the pickledb database
        db = pickledb.load('/code/weather.db', True)

        # Update all the stored database key value pairs
        for key, value in weather.items():
            db.set(key, value)


# Schedule job to update data from API
scheduler = BackgroundScheduler(timezone='US/Eastern')
scheduler.add_job(func=get_current, trigger="interval", minutes=5)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


# API resource for retrieving locally stored weather data
class Weather(Resource):

    # Initialize by loading database
    def __init__(self):
        self.db = pickledb.load('/code/weather.db', True)

    # GET current weather data
    def get(self):
        weather = {
            "time" : self.db.get('time'),
            "temp" : self.db.get('temp'),
            "min_temp" : self.db.get('min_temp'),
            "max_temp" : self.db.get('max_temp'),
            "humidity" : self.db.get('humidity'),
            "icon" : self.db.get('icon'),
            "desc" : self.db.get('desc'),
            "wind_spd" : self.db.get('wind_spd'),
            "wind_dir" : self.db.get('wind_dir'),
            "cloud_cvr" : self.db.get('cloud_cvr'),
            "sunrise" : self.db.get('sunrise'),
            "sunset" : self.db.get('sunset')
        }

        return {'message': 'Success', 'data': weather}, 200


# Add API resource locations
api.add_resource(Weather, '/weather')
