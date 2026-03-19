"""
File: simulated.py

About: This code runs the backend for our adaptive feedback system and plays 
        the beep sound when recieving a request
"""
from flask import Blueprint, jsonify, request
import pygame

simulated_bp = Blueprint("simluated", __name__)

SIM_API_KEY = "simkey"


def beep(duration_ms):
    pygame.mixer.init()
    pygame.mixer.music.load("beep.mp3")
    pygame.mixer.music.play(-1)
    pygame.time.wait(duration_ms)
    pygame.mixer.music.stop()

@simulated_bp.route("")
def simulated():
    return "Simulated Page..."

@simulated_bp.route("get_data", methods=["POST"])
def sim_get_data():
    client_key= request.headers.get("X-SIM-API-KEY")
    if client_key != SIM_API_KEY:
        return jsonify({"error": "Unauthorised"}), 401
    
    if not request.is_json:
        return jsonify({"error": "request must be json"}), 400

    data = request.get_json()
    print(data)
    return jsonify({
        "status": "success",
        "recieved": data
    }), 200

@simulated_bp.route("/alert", methods=["POST"])
def sim_emergency():
    client_key= request.headers.get("X-SIM-API-KEY")
    if client_key != SIM_API_KEY:
        return jsonify({"error": "Unauthorised"}), 401
    
    if not request.is_json:
        return jsonify({"error": "request must be json"}), 400

    data = request.get_json()
    print(f"DATA: {data}")

    try:
        beep(2500)
    except Exception as e:
        print(f"BEEP ERROR: {e}")
    print("ALERT!!!\nALERT!!!!!")
    
    return jsonify({
        "status": "success",
        "recieved": data
    }), 200