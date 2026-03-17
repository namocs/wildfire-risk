"""
File: functions.py

About: This file will contain useful functions that will be used in other files
       for example a functoin that plays a beep sound and a function that displays colour and text
       on the terminal
"""
import requests
import pygame
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
    
