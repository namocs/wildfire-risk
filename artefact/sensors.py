"""
File: sensors.py

About: This code will retrieve the data from the sensors and store them in a csv
       in data/sensorData.csv
"""
from functions import add_to_csv
from datetime import datetime
import adafruit_dht
import board
import requests
import pandas as pd
import os


WIND_PIN = 17
try:
    import RPi.GPIO as GPIO
    HAS_GPIO = True
except ModuleNotFoundError:
    GPIO = True
    HAS_GPIO = False
    print("RPI.GPIO not found")

if HAS_GPIO:
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(WIND_PIN, GPIO.IN)
    except Exception as e:
        print(f"GPIO setup failed: {e}")
        HAS_GPIO = False
else:
    print("Skipping GPIO")

LATITUDE = 51.889807
LONGITUDE = -8.472778
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "data/csv", "sensorData.csv")

dht = adafruit_dht.DHT11(board.D4)


def setup_GPIO():
    if not HAS_GPIO:
        return
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(WIND_PIN, GPIO.IN)

def get_temperature():
    try:
        temp = dht.temperature
        if temp is not None:
            print(f"Temperature: {temp} C")
            return float(temp)
    except RuntimeError as e:
        print(f"Temprature read error: {e}")
    return 0.0

def get_relative_humidity():
    try:
        humid = dht.humidity
        if humid is not None:
            print(f"Humidity: {humid}%")
            return float(humid)
    except RuntimeError as e:
        print(f"Humidity read error: {e}")
    return 0.0

def get_wind_digital():
    if not HAS_GPIO:
        return 0
    try:
        return GPIO.input(WIND_PIN)
    except Exception as e:
        print(f"Wind GPIO read error: {e}")
        return 0

def get_wind_speed():
    wind_digital = get_wind_digital()

    if wind_digital == 0:
        return 0.0
    
    return 33.0
    
# Getting Rainfall from API sine my school doesnn't have a rainfall sensor
def get_rainfall():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": "precipitation",        
        "timezone": "Europe/Dublin",
    }
    resp = requests.get(url=url, params=params, timeout=5)
    data = resp.json()["current"]["precipitation"]
    return data

# This will bundle all the collected data together
def collect_data():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
        "is_windy": get_wind_digital(),
    }

def start():
    row = collect_data()
    add_to_csv(CSV_FILE, row)
    print(f"Collected sensor weather data...") # Digital Output


