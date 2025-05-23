
from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/threats")
def api_threats():
    try:
        with open("mock_threat_data.json") as f:
            data = json.load(f)
            threats = data.get("threats", [])
    except Exception as e:
        print("Error loading mock data:", e)
        threats = []

    search = request.args.get("search", "").lower()
    threat_type = request.args.get("type", "").lower()
    publisher = request.args.get("publisher", "").lower()
    severity = request.args.get("severity", "").lower()

    filtered_data = []
    for threat in threats:
        name = threat.get("name", "").lower()
        t_type = threat.get("type", "").lower()
        pub = threat.get("publisher", "").lower()
        sev = threat.get("severity", "").lower()

        if (search in name and
            (not threat_type or threat_type == t_type) and
            (not publisher or publisher == pub) and
            (not severity or severity == sev)):
            filtered_data.append(threat)

    return jsonify({"threats": filtered_data})
