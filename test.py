import requests

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude":             51.889807,
    "longitude":            -8.472778,
    "minutely_15":          "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,sunshine_duration",
    "timezone":             "Europe/Dublin",
    "wind_speed_unit":      "kmh",
    "past_minutely_15":     96,   # 96 x 15min = 24 hours of past data
    "forecast_minutely_15": 0     # no future predictions
}

response = requests.get(url, params=params)
data = response.json()

m = data["minutely_15"]

reading = {
    "timestamp":             m["time"][-1],
    "temperature_c":         m["temperature_2m"][-1],
    "sunshine_hours":        round((m["sunshine_duration"][-1] or 0) / 3600, 4),
    "relative_humidity_pct": m["relative_humidity_2m"][-1],
    "wind_speed_kmh":        m["wind_speed_10m"][-1],
    "rainfall_mm":           m["precipitation"][-1],
}

print(reading)