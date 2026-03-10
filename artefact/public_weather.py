"""
File: public_weather.py

About: This code will retrieve data from an API service called open-meteo.com 
       I will be fetching the variables I have listed in the todo file and the writing this
       to data/publicData.csv

"""
import requests

url = 'https://api.open-meteo.com/v1/forecast'

params = {
    "latitude": 51.889807,
    "longitude": -8.472778,
    "minutely_15": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,sunshine_duration",
    "timezone": "Europe/Dublin",
    "wind_speed_unit": "kmh",
    "forecast_minutely_15": 0
}

response = requests.get(url, params=params)
data = response.json()
print(data)
m = data["minutely_15"]

readings = {
    "timestamp": m["time"][-1],
    "temperature_c ": m["temperature_2m"][-1],
}

print(readings)

