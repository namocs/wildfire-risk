"""
File: simeulate_data.py

About: This will insert simulated weather data into data/simulatedData.csv, so that we will be able
       to see what the wildfire risk would look like if the data was completely different
"""
from functions import add_to_csv
from datetime import datetime
import pandas as pd
import random
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "data", "simulatedData.csv")

def simulate_data():
    chance = random.choices(
        ["extreme", "high", "moderate"],
        weights=[50, 35, 15]
    )[0]

    if chance == "extreme":
        temperature = round(random.uniform(35.0, 45.0), 1)
        relative_humidity = round(random.uniform(5.0, 15.0), 1)
        wind_speed = round(random.uniform(40.0, 80.0), 1)
        rainfall = 0.0

    elif chance == "high":
        temperature = round(random.uniform(28.0, 35.0), 1)
        relative_humidity = round(random.uniform(15.0, 30.0), 1)
        wind_speed = round(random.uniform(20.0, 40.0), 1)
        rainfall = round(random.uniform(0.0, 0.5), 1)

    else:
        temperature = round(random.uniform(20.0, 28.0), 1)
        relative_humidity = round(random.uniform(30.0, 50.0), 1)
        wind_speed = round(random.uniform(10.0, 20.0), 1)
        rainfall = round(random.uniform(0.0, 2.0), 1)
    
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": temperature,
        "relative_humidity_pct": relative_humidity,
        "wind_speed_kmh": wind_speed,
        "rainfall_mm": rainfall,
        "is_raining": 1 if rainfall > 0.1 else 0,
        "scenario": chance
    }
    
def start():
    row = simulate_data()
    add_to_csv(CSV_FILE, row)
    print("Collected simulated weather data...")
