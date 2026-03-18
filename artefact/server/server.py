from flask import Flask, request, jsonify

app = Flask(__name__)
API_KEY = "supersecret"

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
    app.run(debug=True, port=5000, host="0.0.0.0")