"""
File: risk_model.py

About: This code will pull all the data from the csv that it's give and it will
       crate a risk model 
"""
from datetime import datetime, timedelta
from functions import load_json, save_json
import pandas as pd
import json
import time
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROW_JSON = os.path.join(BASE_DIR, "data/json", "each_row.json")
WINDOW_JSON = os.path.join(BASE_DIR, "data/json", "every_thirty.json")

def next_id(records):
   if not records:
      return 1
   return records[-1]["id"] + 1

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


def load_data(csv_path1, csv_path2=None):
   df1 = pd.read_csv(csv_path1)
   print(f"Model: Loaded {len(df1)} rows from {os.path.basename(csv_path1)}")
   if csv_path2:
      df2 = pd.read_csv(csv_path2)
      print(f"Model: Loaded {len(df2)} rows from {os.path.basename(csv_path2)}")
      df = pd.concat([df1, df2], ignore_index=True)
      print(f"Model: Combined Total: {len(df)} rows")
   else:
      df = df1
   
   df["timestamp"] = pd.to_datetime(df["timestamp"])

   df = df.groupby("timestamp").mean(numeric_only=True).reset_index()
   df = df.sort_values("timestamp").reset_index(drop=True)

   return df


# Calculates Risk each time a row is added
def row_model(csv_path1, csv_path2=None):
   last_seen = None
   row_counter = 0
   source = os.path.basename(csv_path1).replace(".csv", "")
   if csv_path2:
      source = os.path.basename(csv_path1).replace(".csv", "") + " + " + os.path.basename(csv_path2).replace(".csv", "") + " (combined)"

   time.sleep(30) # Wait 30 seconds for data collectors to run
   while True:
      try:
         df = load_data(csv_path1, csv_path2)
         new_rows = df[df["timestamp"] > last_seen] if last_seen is not None else df
         records = load_json(ROW_JSON)

         for _, row in new_rows.iterrows():
            risk = calculate_risk(
               row["temperature"],
               row["relative_humidity_pct"],
               row["wind_speed_kmh"],
               row["rainfall_mm"]
            )
            label = get_risk_label(risk)
            ts = row["timestamp"].strftime("%Y-%m-%d %H:%M")
            record = {
               "id": next_id(records),
               "timestamp": ts,
               "time_range": ts,
               "risk_label": label,
               "percentage": f"{risk}%",
               "float": round(risk / 100, 2),
               "source": source,
            }

            records.append(record)
            print(f"Row: {ts} {risk}% {label}")

            row_counter += 1
            if row_counter % 2 == 0:
               run_window(csv_path1, csv_path2)
         
         if not new_rows.empty:
            last_seen = new_rows["timestamp"].max()
            save_json(ROW_JSON, records)

      except Exception as e:
         print(f"ERROR: At row_model: {e}")

      time.sleep(300)

# Calculates risk model that runs every 30 minutes
def run_window(csv_path1, csv_path2):
   source = os.path.basename(csv_path1).replace(".csv", "")
   if csv_path2:
      source = os.path.basename(csv_path1).replace(".csv", "") + " + " + os.path.basename(csv_path2).replace(".csv", "") + " (combined)"

   try:
      df = load_data(csv_path1, csv_path2)
      windows = df.set_index("timestamp").resample("30min").mean(numeric_only=True).dropna()
      windows = windows.reset_index()

      if not windows.empty:
         latest = windows.iloc[-1]
         window_end = latest["timestamp"]
         window_start = window_end - timedelta(minutes=30)
         risk = calculate_risk(
            latest["temperature"],
            latest["relative_humidity_pct"],
            latest["wind_speed_kmh"],
            latest["rainfall_mm"]
         )
         label = get_risk_label(risk)
         records = load_json(WINDOW_JSON)
         record = {
            "id": next_id(records),
            "timestamp": window_end.strftime("%Y-%m-%d %H:%M"),
            "time_range": f"{window_start.strftime('%H:%M')} - {window_end.strftime('%H:%M')}",
            "risk_label": label,
            "percentage": f"{risk}%",
            "float": round(risk / 100, 2),
            "source": source,
         }

         records.append(record)
         save_json(WINDOW_JSON, records)

         print(f"30 min windows - {record['time_range']}\nRisk: {risk}% - {label}")

   except Exception as e:
      print(f"ERROR: At run_window: {e} ")