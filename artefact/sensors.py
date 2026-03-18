"""
File: sensors.py

About: This code will retrieve the data from the sensors and store them in a csv
       in data/sensorData.csv.
"""
from functions import add_to_csv
from datetime import datetime
import pandas as pd
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "data", "sensorData.csv")

def get_temperature():
    print("Getting temperature data ")
    return 10.0 

def get_relative_humidity():
    print("Getting Relative Humidity Data in %")
    return 20.0

def get_wind_speed():
    print("Getting Wind Speed in km/h")
    return 33.0

def get_rainfall():
    print("Getting Rainfall data in mm")
    return 33.0


timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# This will bundle all the collected data together
def collect_data():
    temperature = float(get_temperature())
    relative_humidity = float(get_relative_humidity())
    wind_speed = float(get_wind_speed())
    rainfall = float(get_rainfall())

    return {
        "timestamp": timestamp,
        "temperature": temperature,
        "relative_humidity_pct": relative_humidity,
        "wind_speed_kmh": wind_speed,
        "rainfall_mm": rainfall,
        "is_raining": 1 if rainfall > 0.1 else 0,
    }

def start():
    row = collect_data()
    add_to_csv(CSV_FILE, row)
    print(f"Collected sensor weather data...") # Digital Output


