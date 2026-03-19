"""
File: functions.py

About: This file will contain useful functions that will be used in other files
       for example a functoin that plays a beep sound and a function that displays colour and text
       on the terminal
"""
from dotenv import load_dotenv
import pandas as pd
import requests
import pygame
import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BEEP_FILE = os.path.join(BASE_DIR, "assets", "beep.mp3")

load_dotenv()


def beep(duration_ms):
    pygame.mixer.init()
    pygame.mixer.music.load(BEEP_FILE)
    pygame.mixer.music.play(-1)
    pygame.time.wait(duration_ms)
    pygame.mixer.music.stop()


# An Adaptive Feedback system!!
def send_alert(record):
    if record["risk_label"] not in ["VERY HIGH", "EXTREME"]:
        return
    
    flask_ip = os.getenv("FLASK_IP")
    flask_port = os.getenv("FLASK_PORT")
    api_key = os.getenv("MAIN_API_KEY")
    flask_url = f"http://{flask_ip}:{flask_port}/alert"
    try:
        resp = requests.post(
            url=f"{flask_url}",
            json=record,
            headers={"X-API-KEY": api_key},
            timeout= 5
        )
        print(f"ALERT SENT: {resp.status_code}")
    except Exception as e:
        print(f"SEND ALERT ERROR: ALERT ERROR: {e}")



def add_to_csv(path, row):
    file_exists = os.path.exists(path)
    data = pd.DataFrame([row])
    data.to_csv(
        path,
        mode="a",
        header=not file_exists,
        index=False,
        encoding="utf-8"
    )
    
def load_json(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            info = f.read().strip()
            if not info:
                return []
            return json.loads(info)
    except json.JSONDecodeError:
        return []
    

def save_json(path, data):
    with open(path,"w") as f:
        json.dump(data, f, indent=4)

def next_id(records):
    return records[-1]["id"] + 1 if records else 1

