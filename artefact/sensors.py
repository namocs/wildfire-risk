"""
File: sensors.py

About: This code will retrieve the data from the sensors and store them in a csv
       in data/sensorData.csv.
"""
from datetime import datetime
import pandas as pd
import os


CSV_FILE = "data/sensorData.csv"

def get_temperature():
    print("Getting temperature data ")
    return 10.0 

def get_sunshine():
    print("Getting Sunshine Datra in hours")
    return 3.0

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
    sunshine = float(get_sunshine())
    relative_humidity = float(get_relative_humidity())
    wind_speed = float(get_wind_speed())
    rainfall = float(get_rainfall())

    return {
        "timestamp": timestamp,
        "temperature": temperature,
        "sunshine_hours": sunshine,
        "relative_humidity_pct": relative_humidity,
        "wind_speed_kmh": wind_speed,
        "rainfall_mm": rainfall,
    }


def add_to_csv(path, row):
    file_exists = os.path.exists(path)
    data = pd.DataFrame([row])
    data.to_csv(
        path,
        mode="a",
        header=not file_exists,
        index=False,
        encoding="utf=8"
    )


def start():
    print(f"Collecting Data...")
    row = collect_data()
    add_to_csv(CSV_FILE, row)

