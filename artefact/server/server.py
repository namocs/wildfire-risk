"""
File: server.py

About: This will run the flask web server and recieve data from the raspberry pi model
       and display the statistics to the user.
"""
from flask import Flask, request, jsonify
from simulated import simulated_bp
import pygame

app = Flask(__name__)
API_KEY = "serverkey"

def beep(duration_ms):
    pygame.mixer.init()
    pygame.mixer.music.load("beep.mp3")
    pygame.mixer.music.play(-1)
    pygame.time.wait(duration_ms)
    pygame.mixer.music.stop()


app.register_blueprint(simulated_bp, url_prefix="/simulated")

@app.route("/")
def main():
    return "Home Page"


@app.route("/alert", methods=["POST"])
def alrt():
    client_key= request.headers.get("X-API-KEY")
    if client_key != API_KEY:
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

if __name__ == "__main__":
    app.run(debug=True, port=8000, host="0.0.0.0")