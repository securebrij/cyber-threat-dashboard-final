 HEAD
from flask import Flask, render_template, jsonify, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

MOCK_DATA = [
    {
        "name": "PhishTank - Dynamic List of Verified/Online Banking Phishing URLs",
        "location": {
            "city": "Los Angeles",
            "country": "United States",
            "lat": 34.0522,
            "lon": -118.2437
        },
        "ip": "156.236.76.90",
        "type": "Phishing",
        "publisher": "VertekLabs",
        "created": "2025-05-15T10:00:00",
        "severity": "Medium"
    },
    {
        "name": "PhishTank - Dynamic List of Verified/Online Banking Phishing URLs",
        "location": {
            "city": "London",
            "country": "United Kingdom",
            "lat": 51.5074,
            "lon": -0.1278
        },
        "ip": "198.105.127.124",
        "type": "Phishing",
        "publisher": "VertekLabs",
        "created": "2025-05-14T09:00:00",
        "severity": "High"
    },
    {
        "name": "PhishTank - Dynamic List of Verified/Online Banking Phishing URLs",
        "location": {
            "city": "Taichung",
            "country": "Taiwan",
            "lat": 24.1477,
            "lon": 120.6736
        },
        "ip": "218.187.69.59",
        "type": "Phishing",
        "publisher": "VertekLabs",
        "created": "2025-05-13T11:30:00",
        "severity": "Low"
    }
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/threats")
def get_threats():
    search = request.args.get("search", "").lower()
    threat_type = request.args.get("type")
    publisher = request.args.get("publisher")
    severity_filter = request.args.get("severity")
    sort_by = request.args.get("sort")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    filtered = MOCK_DATA

    if search:
        filtered = [t for t in filtered if search in t["name"].lower()]
    if threat_type and threat_type != "All":
        filtered = [t for t in filtered if t["type"] == threat_type]
    if publisher and publisher != "All":
        filtered = [t for t in filtered if t["publisher"] == publisher]
    if severity_filter and severity_filter != "All":
        filtered = [t for t in filtered if t["severity"] == severity_filter]

    if sort_by == "severity":
        severity_order = {"High": 3, "Medium": 2, "Low": 1}
        filtered.sort(key=lambda t: severity_order.get(t["severity"], 0), reverse=True)
    elif sort_by == "date":
        filtered.sort(key=lambda t: t.get("created", ""), reverse=True)

    total_threats = len(filtered)
    start = (page - 1) * per_page
    end = start + per_page
    paginated = filtered[start:end]

    chart_data = {
        "severity": {},
        "publisher": {},
        "timeline": {}
    }

    for threat in filtered:
        sev = threat.get("severity", "Unknown")
        pub = threat.get("publisher", "Unknown")
        date = datetime.strptime(threat.get("created"), "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")

        chart_data["severity"][sev] = chart_data["severity"].get(sev, 0) + 1
        chart_data["publisher"][pub] = chart_data["publisher"].get(pub, 0) + 1
        chart_data["timeline"][date] = chart_data["timeline"].get(date, 0) + 1

    return jsonify({
        "threats": paginated,
        "total": total_threats,
        "page": page,
        "per_page": per_page,
        "chart_data": chart_data
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)


from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/threats')
def threats():
    try:
        with open('mock_data.json') as f:
            data = json.load(f)
    except Exception as e:
        data = []
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(debug=True, host='0.0.0.0', port=port)
 cbc0918 (✅ Push working version with fixed chart rendering and fallbacks)
