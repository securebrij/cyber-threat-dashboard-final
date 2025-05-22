import os
import json
import requests
from flask import Flask, render_template, jsonify, request, Response
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def geolocate_ip(ip):
    try:
        response = requests.get(f"https://ip-api.com/json/{ip}", timeout=5)
        data = response.json()
        if data["status"] == "success":
            return {
                "lat": data["lat"],
                "lon": data["lon"],
                "city": data.get("city", "Unknown"),
                "country": data.get("country", "Unknown")
            }
    except Exception as e:
        print(f"Geo error for {ip}:", e)
    return {"lat": None, "lon": None, "city": "Unknown", "country": "Unknown"}

def fetch_live_threats():
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    headers = {"X-OTX-API-KEY": os.getenv("OTX_API_KEY")}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        threats = []
        for pulse in data.get("results", []):
            for ind in pulse.get("indicators", []):
                if ind.get("type") == "IPv4":
                    geo = geolocate_ip(ind["indicator"])
                    threats.append({
                        "name": pulse.get("name", "Unnamed"),
                        "ip": ind["indicator"],
                        "publisher": pulse.get("author_name", "Unknown"),
                        "severity": "High",
                        "type": ind["type"],
                        "created": pulse.get("created", datetime.utcnow().isoformat()),
                        "location": geo
                    })
        return threats
    except Exception as e:
        print("Live fetch failed:", e)
        return []

def load_mock_data():
    try:
        with open("mock_threat_data.json") as f:
            return json.load(f).get("threats", [])
    except Exception as e:
        print("Mock load failed:", e)
        return []

def build_chart_data(threats):
    chart_data = {
        "publisher": {},
        "severity": {},
        "timeline": {}
    }
    for t in threats:
        pub = t.get("publisher", "Unknown")
        sev = t.get("severity", "Unknown")
        day = t.get("created", "")[:10]
        chart_data["publisher"][pub] = chart_data["publisher"].get(pub, 0) + 1
        chart_data["severity"][sev] = chart_data["severity"].get(sev, 0) + 1
        chart_data["timeline"][day] = chart_data["timeline"].get(day, 0) + 1
    return chart_data

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/threats")
def api_threats():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    pub = request.args.get("publisher")
    typ = request.args.get("type")
    sev = request.args.get("severity")

    threats = fetch_live_threats()
    if not threats:
        threats = load_mock_data()

    # Filters
    if pub:
        threats = [t for t in threats if t.get("publisher") == pub]
    if typ:
        threats = [t for t in threats if t.get("type") == typ]
    if sev:
        threats = [t for t in threats if t.get("severity") == sev]

    # Pagination
    total = len(threats)
    start = (page - 1) * per_page
    end = start + per_page
    page_data = threats[start:end]

    return jsonify({
        "threats": page_data,
        "page": page,
        "per_page": per_page,
        "total": total,
        "chart_data": build_chart_data(threats)
    })

@app.route("/export")
def export_csv():
    threats = fetch_live_threats()
    if not threats:
        threats = load_mock_data()
    header = ["name", "ip", "type", "publisher", "severity", "created", "lat", "lon"]
    lines = [",".join(header)]
    for t in threats:
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
        lines.append(",".join(row))
    return Response("\n".join(lines), mimetype="text/csv",
                    headers={"Content-disposition": "attachment; filename=threats.csv"})

if __name__ == "__main__":
    app.run(debug=True)