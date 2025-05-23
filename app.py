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
    except:
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
                        "title": pulse.get("name"),
                        "ip": ind["indicator"],
                        "publisher": pulse.get("author_name", "Unknown"),
                        "severity": "High",
                        "type": ind["type"],
                        "timestamp": pulse.get("created", datetime.utcnow().isoformat()),
                        "latitude": geo.get("lat"),
                        "longitude": geo.get("lon")
                    })
        return threats
    except Exception as e:
        print("Live fetch failed:", e)
        return []

def load_mock_data():
    try:
        with open("mock_threat_data.json") as f:
            return json.load(f)
    except:
        return []

def build_chart_data(threats):
    chart = {"severity": {}, "publisher": {}, "timeline": {}}
    for t in threats:
        sev = t.get("severity", "Unknown")
        pub = t.get("publisher", "Unknown")
        date = t.get("timestamp", "")[:10]
        chart["severity"][sev] = chart["severity"].get(sev, 0) + 1
        chart["publisher"][pub] = chart["publisher"].get(pub, 0) + 1
        chart["timeline"][date] = chart["timeline"].get(date, 0) + 1
    return chart

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/threats")
def api_threats():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    severity = request.args.get("severity")
    publisher = request.args.get("publisher")
    ttype = request.args.get("type")

    threats = fetch_live_threats() or load_mock_data()

    if severity:
        threats = [t for t in threats if t["severity"] == severity]
    if publisher:
        threats = [t for t in threats if t["publisher"] == publisher]
    if ttype:
        threats = [t for t in threats if t["type"] == ttype]

    total = len(threats)
    start = (page - 1) * per_page
    end = start + per_page
    return jsonify({
        "threats": threats[start:end],
        "total": total,
        "page": page,
        "per_page": per_page,
        "chart_data": build_chart_data(threats)
    })

@app.route("/export")
def export_csv():
    threats = fetch_live_threats() or load_mock_data()
    output = ["title,ip,type,publisher,severity,timestamp,latitude,longitude"]
    for t in threats:
        row = [t.get("title",""), t.get("ip",""), t.get("type",""), t.get("publisher",""),
               t.get("severity",""), t.get("timestamp",""),
               str(t.get("latitude","")), str(t.get("longitude",""))]
        output.append(",".join(row))
    return Response("\n".join(output), mimetype="text/csv",
                    headers={"Content-disposition": "attachment; filename=threats.csv"})

if __name__ == "__main__":
    app.run(debug=True)