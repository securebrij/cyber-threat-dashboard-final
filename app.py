from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)

# Load mock data
def load_mock_data():
    try:
        with open("mock_threat_data.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print("Error loading mock data:", e)
        return {"threats": [], "chart_data": {}}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/threats")
def api_threats():
    data = load_mock_data()

    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    publisher = request.args.get("publisher")
    threat_type = request.args.get("type")
    severity = request.args.get("severity")

    threats = data.get("threats", [])

    # Apply filters
    if publisher:
        threats = [t for t in threats if t.get("publisher") == publisher]
    if threat_type:
        threats = [t for t in threats if t.get("type") == threat_type]
    if severity:
        threats = [t for t in threats if t.get("severity") == severity]

    # Paginate
    total = len(threats)
    start = (page - 1) * per_page
    end = start + per_page
    paginated = threats[start:end]

    return jsonify({
        "threats": paginated,
        "page": page,
        "per_page": per_page,
        "total": total,
        "chart_data": data.get("chart_data", {})
    })

@app.route("/export")
def export_csv():
    from flask import Response
    import csv
    data = load_mock_data()["threats"]
    output = []
    header = ["name", "ip", "type", "publisher", "severity", "created", "lat", "lon"]

    output.append(",".join(header))
    for t in data:
        row = [
            t.get("name", ""),
            t.get("ip", ""),
            t.get("type", ""),
            t.get("publisher", ""),
            t.get("severity", ""),
            t.get("created", ""),
            str(t.get("location", {}).get("lat", "")),
            str(t.get("location", {}).get("lon", ""))
        ]
        output.append(",".join(row))

    return Response("\n".join(output), mimetype="text/csv", headers={"Content-disposition": "attachment; filename=threats.csv"})

if __name__ == "__main__":
    app.run(debug=True)