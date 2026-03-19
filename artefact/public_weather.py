"""
File: public_weather.py

About: This code will retrieve data from an API service called open-meteo.com 
       I will be fetching the variables I have listed in the todo file and the writing this
       to data/publicData.csv

"""
from functions import add_to_csv
from datetime import datetime
import requests
import os
import pandas as pd
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "data/csv", "publicData.csv")
LATITUDE = 51.889807
LONGITUDE = -8.472778


def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",        
        "timezone": "Europe/Dublin",
        "wind_speed_unit": "kmh",
    }
    resp = requests.get(url=url, params=params, timeout=5)
    data = resp.json()
    print(f"RESPONSE  CODE: {resp.status_code}")
    print(f"RAW DATA: {data["current"]}")
    return data["current"]


def collect_data():
    m = get_weather()
    raw_time = m["time"]
    # timestamp = datetime.strptime(raw_time, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    wind = m["wind_speed_10m"]
    return {
        "timestamp": timestamp,
        "temperature": m["temperature_2m"],
        "relative_humidity_pct": m["relative_humidity_2m"],
        "wind_speed_kmh": m["wind_speed_10m"],
        "rainfall_mm": m["precipitation"],
        "is_windy": 1 if wind > 20 else 0
    }

def start():
    row = collect_data()
    add_to_csv(CSV_FILE, row)
    print("Collected public weather data...") # Digital Output

