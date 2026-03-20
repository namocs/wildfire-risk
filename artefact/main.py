"""
File: main.py

About: This code will run the collection data for public weather data, sensor and simulated data.
       It will be running every 15 minutes until this program is stopped and our model will also
       check for the risk and send ata
"""
import threading
import time

import public_weather
import simulate_data
import risk_model
import sensors
import functions
import os

INTERVAL = 900 # Runs every 15 minutes due to Open-Meteo's latest weather data which is only every 15 mins
PUBLIC_CSV = os.path.join(os.path.dirname(__file__), "data/csv", "publicData.csv")
SIMULATED_CSV = os.path.join(os.path.dirname(__file__), "data/csv", "simulatedData.csv")
SENSOR_CSV = os.path.join(os.path.dirname(__file__), "data/csv", "sensorData.csv")

def run_func(func, name):
    x = 0
    while True:
        try:
            x += 1
            func()
            functions.beep(2000) # Digital Output (Beep Noise)
            print(f"Count: {x}")
        except Exception as e:
            print(f"{name} Error: {e}")
        time.sleep(INTERVAL)




# Run Data Collection
threading.Thread(target=run_func, args=(public_weather.start, "Pubic Wather")).start()
threading.Thread(target=run_func, args=(sensors.start, "Sensor Data")).start()
threading.Thread(target=run_func, args=(simulate_data.start, "Simulated Weather")).start()


# Run Risk Model
time.sleep(5) # Start Model after short delay
threading.Thread(target=risk_model.row_model, args=(PUBLIC_CSV,SIMULATED_CSV)).start()
