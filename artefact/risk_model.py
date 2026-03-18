"""
File: risk_model.py

About: This code will pull all the data from the csv that it's give and it will
       crate a risk model 
"""
from datetime import datetime, timedelta
import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROW_JSON = os.path.join(BASE_DIR, "data/json", "each.json")
WINDOW_JSON = os.path.join(BASE_DIR, "data/json", "thirty.json")

def calculate_risk(temperature, relative_humidity, wind_speed, rainfall):
    temperature_score = max(0.0, min(1.0, (temperature - 10) / 30))
    humidity_score = max(0.0, min(1.0, (80 - relative_humidity) / 60))
    wind_score = max(0.0, min(1.0, wind_speed / 60))
    rain_score = max(0.0, min(1.0, 1 - (rainfall / 10)))

    risk_score = (
       humidity_score * 0.35 +
       temperature_score * 0.30 +
       wind_score * 0.25 +
       rain_score * 0.10
    )

    return round(risk_score * 100, 1)

def get_risk_label(risk_pct):
    label = "LOW"
    if risk_pct >= 20:
       label = "MODERATE"
    if risk_pct >= 40:
       label = "HIGH"
    if risk_pct >= 65:
       label = "VERY HIGH"
    if risk_pct>= 85:
       label = "EXTREME"
    
    return label

# Calculates risk for each row
def row_model():
   return "Hello"