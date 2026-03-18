from flask import Blueprint, jsonify, request

simulated_bp = Blueprint("simluated", __name__)

SIM_API_KEY = "simkey"

@simulated_bp.route("")
def simulated():
    return "Simulated Page"

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

@simulated_bp.route("get_data/emergency", methods=[])
def sim_emergency():
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