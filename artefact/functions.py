"""
File: functions.py

About: This file will contain useful functions that will be used in other files
       for example a functoin that plays a beep sound and a function that displays colour and text
       on the terminal
"""
import pandas as pd
import requests
import pygame
import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BEEP_FILE = os.path.join(BASE_DIR, "assets", "beep.mp3")

def beep(duration_ms):
    pygame.mixer.init()
    pygame.mixer.music.load(BEEP_FILE)
    pygame.mixer.music.play(-1)
    pygame.time.wait(duration_ms)
    pygame.mixer.music.stop()

 
def send_data(data):
    return data
    
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
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_json(path, data):
    with open(path,"w") as f:
        json.dump(data, f, indent=4)

def next_id(records):
    return records[-1]["id"] + 1 if records else 1

