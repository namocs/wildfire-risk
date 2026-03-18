"""
File: main.py

About: This code will run the collection data for public weather data, sensor and simulated data.
       It will be running every 10 minutes until this program is stopped and our model will also
       check for the risk and send ata
"""
import threading
import time

import public_weather
import simulate_data
import sensors
import functions

INTERVAL = 300 # Run Every 5 Minutes

def run_func(func, name):
    x = 0
    while True:
        try:
            x += 1
            func()
            # functions.beep(1400) # Digital Output (Beep Noise)
            print(f"Count: {x}")
        except Exception as e:
            print(f"{name} Error: {e}")
        time.sleep(INTERVAL)

threading.Thread(target=run_func, args=(public_weather.start, "Pubic Wather")).start()
threading.Thread(target=run_func, args=(sensors.start, "Sensor Data")).start()
threading.Thread(target=run_func, args=(simulate_data.start, "Simulated Weather")).start()
