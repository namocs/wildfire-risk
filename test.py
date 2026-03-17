"""
File: risk_model.py
About: Calculates wildfire risk per 30 minute window from CSV data
"""
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "artefact/data", "simulatedData.csv")

def calculate_risk(temperature, relative_humidity, wind_speed, rainfall, sunshine_hours):
    temp_score     = max(0.0, min(1.0, (temperature - 10) / 30))
    humidity_score = max(0.0, min(1.0, (80 - relative_humidity) / 60))
    wind_score     = max(0.0, min(1.0, wind_speed / 60))
    rain_score     = max(0.0, min(1.0, 1 - (rainfall / 10)))
    sun_score      = max(0.0, min(1.0, sunshine_hours / 0.25))

    risk_level = (
        humidity_score * 0.35 +
        temp_score     * 0.25 +
        wind_score     * 0.20 +
        rain_score     * 0.10 +
        sun_score      * 0.10
    )
    return round(risk_level, 2)

def get_risk_label(risk_level):
    if risk_level >= 0.85:   return "EXTREME"
    elif risk_level >= 0.65: return "HIGH"
    elif risk_level >= 0.40: return "MODERATE"
    elif risk_level >= 0.20: return "LOW"
    else:                    return "VERY LOW"

def analyse_30min_windows():
    df = pd.read_csv(CSV_FILE)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Group into 30 minute buckets
    df.set_index("timestamp", inplace=True)
    windows = df.resample("30min").mean(numeric_only=True).dropna()

    results = []
    for time, row in windows.iterrows():
        risk = calculate_risk(
            temperature       = row["temperature"],
            relative_humidity = row["relative_humidity_pct"],
            wind_speed        = row["wind_speed_kmh"],
            rainfall          = row["rainfall_mm"],
            sunshine_hours    = row["sunshine_hours"]
        )
        label = get_risk_label(risk)
        results.append({
            "window":                time.strftime("%Y-%m-%d %H:%M"),
            "avg_temperature":       round(row["temperature"], 2),
            "avg_humidity":          round(row["relative_humidity_pct"], 2),
            "avg_wind_speed":        round(row["wind_speed_kmh"], 2),
            "avg_rainfall":          round(row["rainfall_mm"], 2),
            "avg_sunshine_hours":    round(row["sunshine_hours"], 4),
            "risk_level":            risk,
            "risk_pct":              f"{risk * 100:.1f}%",
            "risk_label":            label
        })

    return pd.DataFrame(results)

if __name__ == "__main__":
    df = analyse_30min_windows()
    print(df.to_string(index=False))
