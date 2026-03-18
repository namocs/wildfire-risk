"""
File: server.py

About: This will run the flask web server and recieve data from the raspberry pi model
       and display the statistics to the user.
"""
from flask import Flask, request, jsonify
from simulated import simulated_bp

app = Flask(__name__)
API_KEY = "serverkey"

app.register_blueprint(simulated_bp, url_prefix="/simulated")

@app.route("/")
def main():
    return "Home Page"


@app.route("/get_data", methods=["POST"])
def get_data():
    client_key= request.headers.get("X-API-KEY")
    if client_key != API_KEY:
        return jsonify({"error": "Unauthorised"}), 401
    
    if not request.is_json:
        return jsonify({"error": "request must be json"}), 400

    data = request.get_json()
    print(data)
    return jsonify({
        "status": "success",
        "recieved": data
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=8000, host="0.0.0.0")