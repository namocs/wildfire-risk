"""
File: simeulate_data.py

About: This will insert simulated weather data into data/simulatedData.csv, so that we will be able
       to see what the wildfire risk would look like if the data was completely different also completes Basic requirments 3 as
       I am simulating data and creating a what if statement and notifying the web server
"""
from dotenv import load_dotenv
from functions import add_to_csv
from datetime import datetime
import pandas as pd
import risk_model
import random
import requests
import time
import os

load_dotenv()

FLASK_IP = os.getenv("FLASK_IP")
FLASK_PORT = os.getenv("FLASK_PORT")

FLASK_ALERT = f"http://{FLASK_IP}:{FLASK_PORT}/simulated//alert"
SIM_API_KEY = os.getenv("SIM_API_KEY")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "data/csv", "simulatedData.csv")



def simulate_data():
    chance = random.choices(
        ["extreme", "high", "moderate"],
        weights=[25, 35, 40]
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
        "is_windy": 1 if wind_speed > 20 else 0,
        "scenario": chance
    }

def send_simulated_alert(row):
    try:
        resp = requests.post(
            url=f"{FLASK_ALERT}",
            json=row,
            headers={"X-SIM-API-KEY": SIM_API_KEY},
            timeout= 5
        )  
        print(f"SIMULATED ALERT SENT: {resp.status_code}")
    except Exception as e:
        print(f"SIM ALERT ERROR: {e}")

sim_row_counter  = 0


def start():
    global sim_row_counter
    row = simulate_data()
    add_to_csv(CSV_FILE, row)
    print("Collected simulated weather data...")

    # Send Data to RPI if "extreme" level scenario
    if row['scenario'] == "extreme":
        send_simulated_alert(row=row)
        print("SENT REQUEST TO SERVER!!!!!!!")
    
    sim_row_counter += 1
    if sim_row_counter % 2 == 0:
        risk_model.run_window(CSV_FILE, json_path=risk_model.SIM_WINDOW_JSON)
        print(f"SIMULATED MODULE: Ran Model after {sim_row_counter} rows")
