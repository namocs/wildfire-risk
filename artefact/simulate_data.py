"""
File: simeulate_data.py

About: This will insert simulated weather data into data/simulatedData.csv, so that we will be able
       to see what the wildfire risk would look like if the data was completely different
"""
from datetime import datetime
import pandas as pd
import random
import time
import os

CSV_FILE = "data/simulatedData.csv"
INTERVAL = 600

def simulate_data():
    chance = random.choices(
        ["extreme", "high", "moderate"],
        weights=[50, 35, 15]
    )[0]

    if chance == "extreme":
        temperature = round(random.uniform(35.0, 45.0), 1)
        sunshine_hours = round(random.uniform(0.20, 0.25), 4)
        relative_humidity = round(random.uniform(5.0, 15.0), 1)
        wind_speed = round(random.uniform(40.0, 80.0), 1)
        rainfall = 0.0

    elif chance == "high":
        temperature = round(random.uniform(28.0, 35.0), 1)
        sunshine_hours = round(random.uniform(0.15, 0.20), 4)
        relative_humidity = round(random.uniform(15.0, 30.0), 1)
        wind_speed = round(random.uniform(20.0, 40.0), 1)
        rainfall = round(random.uniform(0.0, 0.5), 1)

    else:
        temperature = round(random.uniform(20.0, 28.0), 1)
        sunshine_hours = round(random.uniform(0.05, 0.15), 4)
        relative_humidity = round(random.uniform(30.0, 50.0), 1)
        wind_speed = round(random.uniform(10.0, 20.0), 1)
        rainfall = round(random.uniform(0.0, 2.0), 1)
    
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": temperature,
        "sunshine_hours": sunshine_hours,
        "relative_humidity_pct": relative_humidity,
        "wind_speed_kmh": wind_speed,
        "rainfall_mm": rainfall,
        "scenario": chance
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

x = 0
while True:
    try:
        x += 1
        row = simulate_data()
        add_to_csv(CSV_FILE, row)
        print(f"Saved {x} times")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(INTERVAL)