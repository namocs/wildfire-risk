"""
File: functions.py

About: This file will contain useful functions that will be used in other files
       for example a functoin that plays a beep sound and a function that displays colour and text
       on the terminal
"""

import pygame

def beep(duration_ms):
    pygame.mixer.init()
    pygame.mixer.music.load("assets/beep.mp3")
    pygame.mixer.music.play(-1)
    pygame.time.wait(duration_ms)
    pygame.mixer.music.stop()
    
