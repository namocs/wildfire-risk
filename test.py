"""
File: risk_model.py
About: Calculates wildfire risk score from weather variables

References:
[1] Natural Resources Canada — FWI System
    https://cwfis.cfs.nrcan.gc.ca/background/summary/fwi
[2] Van Wagner, C.E. 1987. Canadian Forest Fire Weather Index System.
    https://cfs.nrcan.gc.ca/pubwarehouse/pdfs/19927.pdf
"""

import pandas as pd
import os

BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
PUBLIC_CSV    = os.path.join(BASE_DIR, "artefact/data", "publicData.csv")
SENSOR_CSV    = os.path.join(BASE_DIR, "artefact/data", "sensorData.csv")
SIMULATED_CSV = os.path.join(BASE_DIR, "artefact/data", "simulatedData.csv")


def calculate_risk(temperature, relative_humidity, wind_speed, rainfall):
    temp_score     = max(0.0, min(1.0, (temperature - 10)       / 30))
    humidity_score = max(0.0, min(1.0, (80 - relative_humidity) / 60))
    wind_score     = max(0.0, min(1.0,  wind_speed              / 60))
    rain_score     = max(0.0, min(1.0,  1 - (rainfall           / 10)))

    risk_score = (
        humidity_score * 0.35 +
        temp_score     * 0.30 +
        wind_score     * 0.25 +
        rain_score     * 0.10
    )

    return round(risk_score * 100, 1)  # return as percentage e.g. 72.4


def get_risk_label(risk_pct):
    if   risk_pct >= 85: return "EXTREME"
    elif risk_pct >= 65: return "VERY HIGH"
    elif risk_pct >= 40: return "HIGH"
    elif risk_pct >= 20: return "MODERATE"
    else:                return "LOW"


def load_data(csv_path_1, csv_path_2=None):
    df1 = pd.read_csv(csv_path_1)
    print(f"[MODEL] Loaded {len(df1)} rows from {os.path.basename(csv_path_1)}")

    if csv_path_2:
        df2 = pd.read_csv(csv_path_2)
        print(f"[MODEL] Loaded {len(df2)} rows from {os.path.basename(csv_path_2)}")
        df  = pd.concat([df1, df2], ignore_index=True)
        print(f"[MODEL] Combined total: {len(df)} rows")
    else:
        df = df1

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df


def analyse(csv_path_1, csv_path_2=None):
    df = load_data(csv_path_1, csv_path_2)

    # Average every 6 readings (5 mins × 6 = 30 min windows)
    df.set_index("timestamp", inplace=True)
    windows = df.resample("30min").mean(numeric_only=True).dropna()
    windows = windows.reset_index()

    results = []
    for _, row in windows.iterrows():
        risk = calculate_risk(
            row["temperature"],
            row["relative_humidity_pct"],
            row["wind_speed_kmh"],
            row["rainfall_mm"]
        )
        results.append({
            "window":      row["timestamp"].strftime("%Y-%m-%d %H:%M"),
            "temperature": round(row["temperature"],           1),
            "humidity":    round(row["relative_humidity_pct"], 1),
            "wind_kmh":    round(row["wind_speed_kmh"],        1),
            "rainfall_mm": round(row["rainfall_mm"],           2),
            "risk_pct":    f"{risk}%",
            "risk_label":  get_risk_label(risk),
        })

    return pd.DataFrame(results)



if __name__ == "__main__":
    print("=" * 55)
    print("  WILDFIRE RISK MODEL — Cork City, Ireland")
    print("=" * 55)

    df = analyse(PUBLIC_CSV)
    print(df.to_string(index=False))

 ## Look into this