from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

# Load mock or real threat data
def load_threat_data():
    try:
        with open("mock_threat_data.json", "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading mock data: {e}")
        return []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/threats")
def api_threats():
    data = load_threat_data()

    # Apply filters
    threat_type = request.args.get("type")
    publisher = request.args.get("publisher")
    severity = request.args.get("severity")
    search = request.args.get("search", "").lower()

    filtered_data = []
    for threat in data:
        if (not threat_type or threat.get("type") == threat_type) and            (not publisher or threat.get("publisher") == publisher) and            (not severity or threat.get("severity") == severity) and            (not search or search in threat.get("title", "").lower()):
            filtered_data.append(threat)

    return jsonify({"threats": filtered_data})